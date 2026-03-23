"""
Browser-level smoke test for admin -> student dashboard propagation.

Covers these admin actions:
1) Add student
2) Add subject content
3) Add manlib video
4) Add assessment
5) Record payment

Then verifies student portal pages reflect the updates.
"""

from __future__ import annotations

import os
import re
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Optional
from urllib.request import urlopen

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.security import generate_password_hash


ROOT = Path(__file__).resolve().parents[2]
APP_DIR = ROOT / "classdoodle"
DB_PATH = APP_DIR / "data" / "classdoodle.db"
PYTHON_EXE = ROOT / ".venv" / "Scripts" / "python.exe"
BASE_URL = os.environ.get("SMOKE_BASE_URL", "http://127.0.0.1:5000").rstrip("/")
ADMIN_USERNAME = os.environ.get("SMOKE_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("SMOKE_ADMIN_PASSWORD", "SmokeAdmin!2026")
STUDENT_PASSWORD = os.environ.get("SMOKE_STUDENT_PASSWORD", "SmokeStudent!2026")


class SmokeFailure(Exception):
    pass


@dataclass
class SmokeArtifacts:
    token: str
    student_id: Optional[str] = None
    student_name: Optional[str] = None
    content_title: Optional[str] = None
    video_title: Optional[str] = None
    assessment_type: Optional[str] = None
    admin_previous_hash: Optional[str] = None
    admin_created: bool = False


def log(msg: str) -> None:
    print(f"[smoke] {msg}", flush=True)


def ensure_db_initialized() -> None:
    sys.path.insert(0, str(APP_DIR))
    from backend.database import ClassDoodleDB  # pylint: disable=import-outside-toplevel

    ClassDoodleDB()


def set_admin_password(new_password: str) -> tuple[Optional[str], bool]:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT password_hash FROM user_accounts WHERE username=?",
            (ADMIN_USERNAME,),
        ).fetchone()
        new_hash = generate_password_hash(new_password)
        if row:
            previous_hash = row["password_hash"]
            conn.execute(
                "UPDATE user_accounts SET password_hash=?, role='admin' WHERE username=?",
                (new_hash, ADMIN_USERNAME),
            )
            conn.commit()
            return previous_hash, False

        conn.execute(
            "INSERT INTO user_accounts (username, password_hash, role) VALUES (?, ?, 'admin')",
            (ADMIN_USERNAME, new_hash),
        )
        conn.commit()
        return None, True
    finally:
        conn.close()


def restore_admin_password(previous_hash: Optional[str], admin_created: bool) -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        if previous_hash:
            conn.execute(
                "UPDATE user_accounts SET password_hash=?, role='admin' WHERE username=?",
                (previous_hash, ADMIN_USERNAME),
            )
        elif admin_created:
            conn.execute("DELETE FROM user_accounts WHERE username=?", (ADMIN_USERNAME,))
        conn.commit()
    finally:
        conn.close()


def cleanup_artifacts(a: SmokeArtifacts) -> None:
    conn = sqlite3.connect(DB_PATH)
    try:
        if a.video_title:
            conn.execute("DELETE FROM manlib_videos WHERE title=?", (a.video_title,))
        if a.content_title:
            conn.execute("DELETE FROM subject_content WHERE title=?", (a.content_title,))
        if a.student_id:
            conn.execute("DELETE FROM user_accounts WHERE username=?", (a.student_id,))
            conn.execute("DELETE FROM students WHERE student_id=?", (a.student_id,))
        conn.commit()
    finally:
        conn.close()


def wait_for_server(base_url: str, timeout_s: int = 60) -> None:
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            with urlopen(f"{base_url}/health", timeout=3) as resp:
                if resp.status == 200:
                    return
        except Exception:
            pass
        time.sleep(1)
    raise SmokeFailure("Server did not become healthy in time.")


def start_server() -> tuple[subprocess.Popen, Path, Path, object, object]:
    out_log = ROOT / "tmp_smoke_server.out"
    err_log = ROOT / "tmp_smoke_server.err"
    env = os.environ.copy()
    env["HOST"] = "127.0.0.1"
    env["PORT"] = BASE_URL.rsplit(":", 1)[-1]
    env["FLASK_DEBUG"] = "0"
    env["OFFLINE_MODE"] = "1"
    env["PYTHONUNBUFFERED"] = "1"
    out_handle = open(out_log, "w", encoding="utf-8")
    err_handle = open(err_log, "w", encoding="utf-8")
    proc = subprocess.Popen(
        [str(PYTHON_EXE), "classdoodle/web_app.py"],
        cwd=str(ROOT),
        env=env,
        stdout=out_handle,
        stderr=err_handle,
    )
    return proc, out_log, err_log, out_handle, err_handle


def stop_server(proc: subprocess.Popen) -> None:
    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except subprocess.TimeoutExpired:
            proc.kill()


def make_driver() -> webdriver.Chrome:
    os.environ.setdefault("WDM_LOCAL", "1")
    os.environ.setdefault("WDM_SSL_VERIFY", "0")
    os.environ.setdefault("WDM_PROGRESS_BAR", "0")

    chrome_candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    chrome_bin = next((p for p in chrome_candidates if Path(p).exists()), None)
    if not chrome_bin:
        raise SmokeFailure("Chrome browser not found on this machine.")

    options = ChromeOptions()
    options.binary_location = chrome_bin
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1440,1080")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    cached = sorted(
        (ROOT / ".wdm").glob("drivers/chromedriver/**/chromedriver.exe"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if cached:
        driver_path = str(cached[0])
    else:
        driver_path = ChromeDriverManager().install()
    return webdriver.Chrome(service=ChromeService(driver_path), options=options)


def login(driver: webdriver.Chrome, wait: WebDriverWait, username: str, password: str) -> None:
    driver.get(f"{BASE_URL}/login")
    wait.until(EC.presence_of_element_located((By.NAME, "username"))).clear()
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").clear()
    driver.find_element(By.NAME, "password").send_keys(password)
    robust_click(driver, driver.find_element(By.CSS_SELECTOR, "form[action='/login'] button[type='submit']"))


def assert_contains(driver: webdriver.Chrome, needle: str, label: str) -> None:
    if needle not in driver.page_source:
        raise SmokeFailure(f"Expected to find '{needle}' in {label}.")


def robust_click(driver: webdriver.Chrome, element) -> None:
    """Click element even if sticky headers/toasts temporarily intercept normal clicks."""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    try:
        element.click()
    except Exception:
        driver.execute_script("arguments[0].click();", element)


def robust_type(driver: webdriver.Chrome, element, value: str) -> None:
    """Type into inputs/textareas with JS fallback for occasional interactability quirks."""
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
    try:
        element.clear()
    except Exception:
        pass
    try:
        element.send_keys(value)
    except Exception:
        driver.execute_script(
            "arguments[0].value = arguments[1];"
            "arguments[0].dispatchEvent(new Event('input', {bubbles:true}));"
            "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
            element,
            value,
        )


def run_smoke() -> None:
    token = datetime.now().strftime("%Y%m%d%H%M%S%f")
    artifacts = SmokeArtifacts(token=token)
    proc = None
    out_log = None
    err_log = None
    out_handle = None
    err_handle = None
    driver = None
    wait = None

    try:
        log("Initializing database and setting deterministic admin login for smoke test.")
        ensure_db_initialized()
        prev_hash, admin_created = set_admin_password(ADMIN_PASSWORD)
        artifacts.admin_previous_hash = prev_hash
        artifacts.admin_created = admin_created

        log("Starting local server.")
        proc, out_log, err_log, out_handle, err_handle = start_server()
        wait_for_server(BASE_URL, timeout_s=60)
        log("Server is healthy.")

        log("Launching headless browser.")
        driver = make_driver()
        wait = WebDriverWait(driver, 20)

        # ---------- ADMIN FLOW ----------
        log("Admin login.")
        login(driver, wait, ADMIN_USERNAME, ADMIN_PASSWORD)
        wait.until(EC.url_contains("/dashboard"))

        # 1) Add student
        artifacts.student_name = f"Smoke Student {token}"
        log("Adding student from /student/add.")
        driver.get(f"{BASE_URL}/student/add")
        robust_type(driver, wait.until(EC.presence_of_element_located((By.NAME, "name"))), artifacts.student_name)
        robust_type(driver, driver.find_element(By.NAME, "email"), f"smoke.{token}@example.test")
        robust_type(driver, driver.find_element(By.NAME, "phone"), "0712345678")
        Select(driver.find_element(By.NAME, "grade_level")).select_by_visible_text("Grade 12")
        robust_type(driver, driver.find_element(By.NAME, "parent_name"), "Smoke Parent")
        robust_type(driver, driver.find_element(By.NAME, "parent_phone"), "0823456789")
        robust_type(driver, driver.find_element(By.NAME, "parent_email"), f"parent.{token}@example.test")
        for subject in ("Mathematics", "Physical Sciences", "Life Sciences"):
            subject_box = driver.find_element(By.CSS_SELECTOR, f"input[name='subjects'][value='{subject}']")
            driver.execute_script(
                "arguments[0].checked = true; arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
                subject_box,
            )
        robust_type(driver, driver.find_element(By.NAME, "notes"), "Smoke test registration")
        form_state = driver.execute_script(
            "const f=document.querySelector(\"form[action='/student/add']\");"
            "if(!f) return {ok:false, reason:'form missing'};"
            "return {"
            " ok:f.checkValidity(),"
            " name:f.querySelector(\"[name='name']\")?.value || '',"
            " grade:f.querySelector(\"[name='grade_level']\")?.value || '',"
            " subjects:f.querySelectorAll(\"input[name='subjects']:checked\").length"
            "};"
        )
        if not form_state or not form_state.get("ok"):
            raise SmokeFailure(f"Student form invalid before submit: {form_state}")
        robust_click(driver, driver.find_element(By.CSS_SELECTOR, "form[action='/student/add'] button[type='submit']"))
        try:
            WebDriverWait(driver, 2).until(
                lambda d: "/student/" in d.current_url and not d.current_url.endswith("/student/add")
            )
        except TimeoutException:
            flash_texts = [
                e.text.strip()
                for e in driver.find_elements(By.CSS_SELECTOR, ".flash-message")
                if e.text and e.text.strip()
            ]
            if flash_texts:
                err = " | ".join(flash_texts)
            else:
                page_text = re.sub(r"\s+", " ", driver.page_source)
                err = "unknown"
                for pattern in (
                    r"Error:\s*([^<]+)",
                    r"⚠️\s*([^<]+)",
                    r"error[^<]{0,120}",
                ):
                    m_err = re.search(pattern, page_text, flags=re.IGNORECASE)
                    if m_err:
                        err = m_err.group(1).strip() if m_err.groups() else m_err.group(0).strip()
                        break
            raise SmokeFailure(f"Student add did not redirect. Error hint: {err}")
        m = re.search(r"/student/(CD\d+)", driver.current_url)
        if not m:
            raise SmokeFailure(f"Could not parse student id from URL: {driver.current_url}")
        artifacts.student_id = m.group(1)
        log(f"Student created: {artifacts.student_id}")

        # Set known student login
        log("Setting student login password.")
        driver.get(f"{BASE_URL}/admin/student-accounts")
        Select(wait.until(EC.presence_of_element_located((By.NAME, "student_id")))).select_by_value(artifacts.student_id)
        pw = driver.find_element(By.NAME, "password")
        pw.clear()
        pw.send_keys(STUDENT_PASSWORD)
        robust_click(
            driver,
            driver.find_element(By.CSS_SELECTOR, "form[action='/admin/student-accounts/create'] button[type='submit']"),
        )
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert_contains(driver, artifacts.student_id, "student accounts page")

        # 2) Add subject content
        artifacts.content_title = f"SMOKE_CONTENT_{token}"
        content_text = f"Smoke content payload {token}"
        log("Adding subject content from /admin/subject-content.")
        driver.get(f"{BASE_URL}/admin/subject-content")
        Select(wait.until(EC.presence_of_element_located((By.NAME, "subject")))).select_by_visible_text("Mathematics")
        Select(driver.find_element(By.NAME, "content_type")).select_by_value("notes")
        robust_type(driver, driver.find_element(By.NAME, "title"), artifacts.content_title)
        robust_type(driver, driver.find_element(By.NAME, "description"), "Smoke content description")
        robust_type(driver, driver.find_element(By.NAME, "content_text"), content_text)
        robust_click(
            driver,
            driver.find_element(By.CSS_SELECTOR, "form[action='/admin/subject-content/add'] button[type='submit']"),
        )
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 3) Add manlib video
        artifacts.video_title = f"SMOKE_VIDEO_{token}"
        log("Adding manlib video from /admin/manlib.")
        driver.get(f"{BASE_URL}/admin/manlib")
        video_form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form[action='/admin/manlib/add']")))
        Select(video_form.find_element(By.NAME, "subject")).select_by_visible_text("Mathematics")
        robust_click(driver, video_form.find_element(By.CSS_SELECTOR, "input[name='video_type'][value='youtube']"))
        robust_type(driver, video_form.find_element(By.NAME, "title"), artifacts.video_title)
        robust_type(driver, video_form.find_element(By.NAME, "video_url"), "https://youtu.be/dQw4w9WgXcQ")
        robust_click(driver, video_form.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 4) Add assessment
        artifacts.assessment_type = f"SMOKE_ASSESSMENT_{token}"
        log("Recording assessment from /assessments.")
        driver.get(f"{BASE_URL}/assessments")
        wait.until(EC.url_contains("/assessments"))
        assessment_form = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form[action*='assessment/add']")))
        robust_type(driver, assessment_form.find_element(By.NAME, "student_id"), artifacts.student_id)
        Select(assessment_form.find_element(By.NAME, "subject")).select_by_visible_text("Mathematics")
        assess_type_sel = assessment_form.find_element(By.NAME, "assessment_type")
        driver.execute_script(
            "var s=arguments[0],v=arguments[1];"
            "var o=document.createElement('option');o.value=v;o.text=v;s.appendChild(o);s.value=v;",
            assess_type_sel,
            artifacts.assessment_type,
        )
        robust_type(driver, assessment_form.find_element(By.NAME, "score"), "78")
        robust_type(driver, assessment_form.find_element(By.NAME, "max_score"), "100")
        robust_type(driver, assessment_form.find_element(By.NAME, "date"), date.today().isoformat())
        robust_type(driver, assessment_form.find_element(By.NAME, "notes"), "Smoke assessment note")
        robust_click(driver, assessment_form.find_element(By.CSS_SELECTOR, "button[type='submit']"))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # 5) Record payment
        reference = f"SMOKE_PAY_{token}"
        log("Recording payment from /payments.")
        driver.get(f"{BASE_URL}/payments")
        wait.until(EC.presence_of_element_located((By.ID, "paymentForm")))
        driver.execute_script("openPayment(arguments[0], arguments[1]);", artifacts.student_id, artifacts.student_name)
        amount = wait.until(EC.visibility_of_element_located((By.NAME, "amount")))
        amount.clear()
        amount.send_keys("1500")
        Select(driver.find_element(By.NAME, "payment_method")).select_by_visible_text("EFT")
        ref = driver.find_element(By.NAME, "reference")
        ref.clear()
        ref.send_keys(reference)
        robust_click(driver, driver.find_element(By.CSS_SELECTOR, "#paymentForm button[type='submit']"))
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # ---------- STUDENT FLOW ----------
        log("Switching to student account and verifying dashboard propagation.")
        driver.get(f"{BASE_URL}/logout")
        login(driver, wait, artifacts.student_id, STUDENT_PASSWORD)
        wait.until(EC.url_contains("/my-portal"))

        # Student homepage should not be restricted after payment
        if "Account Restricted" in driver.page_source:
            raise SmokeFailure("Student account is still restricted after payment.")

        # Subjects page must show both content and video entries
        driver.get(f"{BASE_URL}/my-portal/subjects")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert_contains(driver, artifacts.content_title, "student subjects page")
        assert_contains(driver, content_text, "student subjects page")
        assert_contains(driver, artifacts.video_title, "student subjects page")

        # Videos page must show new video title
        driver.get(f"{BASE_URL}/my-portal/videos")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert_contains(driver, artifacts.video_title, "student videos page")

        # Progress page must show new assessment type
        driver.get(f"{BASE_URL}/my-portal/progress")
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        assert_contains(driver, artifacts.assessment_type, "student progress page")
        assert_contains(driver, "Mathematics", "student progress page")

        log("PASS: Admin actions reflected correctly across student dashboard pages.")

    except Exception as exc:
        if driver is not None:
            screenshot = ROOT / "smoke_failure.png"
            try:
                driver.save_screenshot(str(screenshot))
                log(f"Failure screenshot saved: {screenshot}")
            except Exception:
                pass
        raise

    finally:
        if driver is not None:
            driver.quit()
        if proc is not None:
            stop_server(proc)
        if out_handle is not None:
            out_handle.close()
        if err_handle is not None:
            err_handle.close()
        cleanup_artifacts(artifacts)
        restore_admin_password(artifacts.admin_previous_hash, artifacts.admin_created)
        if out_log and out_log.exists():
            log(f"Server stdout log: {out_log}")
        if err_log and err_log.exists():
            log(f"Server stderr log: {err_log}")


if __name__ == "__main__":
    try:
        run_smoke()
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"[smoke] FAIL: {e}", flush=True)
        raise SystemExit(1)
