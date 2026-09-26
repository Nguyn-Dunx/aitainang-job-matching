"""Sinh 3 CV gia lap (PDF) phuc vu test Tang 1 trong luc cho CV that co consent.

    python scripts/make_synthetic_cvs.py

Output: tests/fixtures/cv_single_column.pdf, cv_two_column.pdf, cv_missing_sections.pdf
Day la CV SYNTHETIC (nhan vat ao), khong phai du lieu ca nhan that — ghi ro trong
data/DATA_SOURCES.md muc D2.
"""

from pathlib import Path

from fpdf import FPDF

OUT = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
FONT_DIR = Path("C:/Windows/Fonts")
FONT_REGULAR = FONT_DIR / "arial.ttf"
FONT_BOLD = FONT_DIR / "arialbd.ttf"


def make_pdf() -> FPDF:
    pdf = FPDF()
    pdf.add_font("arial", "", str(FONT_REGULAR))
    pdf.add_font("arial", "B", str(FONT_BOLD))
    pdf.set_auto_page_break(auto=True, margin=15)
    return pdf


def heading(pdf: FPDF, text: str) -> None:
    pdf.set_font("arial", "B", 13)
    pdf.cell(0, 8, text, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("arial", "", 11)


def body(pdf: FPDF, text: str) -> None:
    pdf.set_font("arial", "", 11)
    pdf.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")


def cv_single_column() -> None:
    """CV chuan 1 cot, day du section — happy path."""
    pdf = make_pdf()
    pdf.add_page()
    pdf.set_font("arial", "B", 18)
    pdf.cell(0, 12, "NGUYEN VAN AN", new_x="LMARGIN", new_y="NEXT")
    body(pdf, "Email: an.nguyen@example.com | SDT: 0901 234 567 | Ha Noi")
    body(pdf, "Muc tieu nghe nghiep: Backend Developer (Fresher)")
    heading(pdf, "KY NANG")
    body(pdf, "Ngon ngu: Python, JavaScript, SQL\nFramework: Django, React\n"
              "Co so du lieu: PostgreSQL, Redis\nCong cu: Git, Docker, Linux")
    heading(pdf, "HOC VAN")
    body(pdf, "Cu nhan Cong nghe Thong tin — Dai hoc Bach Khoa Ha Noi (2021 - 2025)\nGPA: 3.2/4.0")
    heading(pdf, "KINH NGHIEM LAM VIEC")
    body(pdf, "Thuc tap sinh Backend — Cong ty FPT Software (06/2024 - 12/2024)\n"
              "- Xay dung REST API bang Django cho he thong quan ly don hang\n"
              "- Toi uu truy van PostgreSQL, giam thoi gian phan hoi 30%")
    heading(pdf, "DU AN")
    body(pdf, "Website dat ve xem phim (2024)\n"
              "- Backend: Django, PostgreSQL; Frontend: React\n"
              "- Trien khai bang Docker tren VPS ca nhan")
    heading(pdf, "NGOAI NGU")
    body(pdf, "Tieng Anh: TOEIC 750")
    pdf.output(str(OUT / "cv_single_column.pdf"))


def cv_two_column() -> None:
    """CV 2 cot: trai = lien he + ky nang, phai = kinh nghiem + du an.
    Test kha nang doc dung thu tu cua PyMuPDF sort=True."""
    pdf = make_pdf()
    pdf.add_page()
    pdf.set_font("arial", "B", 18)
    pdf.cell(0, 12, "TRAN THI BICH", new_x="LMARGIN", new_y="NEXT")
    left_x, right_x, col_w = 10, 110, 90
    top = 35

    # Cot trai
    pdf.set_xy(left_x, top)
    pdf.set_font("arial", "B", 12)
    pdf.cell(col_w, 7, "LIEN HE", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("arial", "", 10)
    pdf.multi_cell(col_w, 5, "bich.tran@example.com\n0912 345 678\nDa Nang")
    pdf.set_x(left_x)
    pdf.set_font("arial", "B", 12)
    pdf.cell(col_w, 7, "KY NANG", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("arial", "", 10)
    pdf.multi_cell(col_w, 5, "Java, Spring Boot\nMySQL, MongoDB\nKafka, Docker\nKubernetes, AWS")

    # Cot phai
    pdf.set_xy(right_x, top)
    pdf.set_font("arial", "B", 12)
    pdf.cell(col_w, 7, "KINH NGHIEM", new_x="LMARGIN", new_y="NEXT")
    pdf.set_xy(right_x, pdf.get_y())
    pdf.set_font("arial", "", 10)
    pdf.multi_cell(col_w, 5, "Backend Developer — NashTech (01/2023 - nay)\n"
                            "- Phat trien microservices bang Spring Boot\n"
                            "- Thiet ke API gateway, trien khai tren AWS")
    pdf.set_xy(right_x, pdf.get_y() + 2)
    pdf.set_font("arial", "B", 12)
    pdf.cell(col_w, 7, "DU AN", new_x="LMARGIN", new_y="NEXT")
    pdf.set_xy(right_x, pdf.get_y())
    pdf.set_font("arial", "", 10)
    pdf.multi_cell(col_w, 5, "He thong thanh toan noi bo\n- Java, Spring Boot, Kafka, MySQL")
    pdf.output(str(OUT / "cv_two_column.pdf"))


def cv_missing_sections() -> None:
    """CV xau: khong co muc HOC VAN, khong thong tin lien he, ten muc viet tat."""
    pdf = make_pdf()
    pdf.add_page()
    pdf.set_font("arial", "B", 16)
    pdf.cell(0, 10, "LE MINH CUONG", new_x="LMARGIN", new_y="NEXT")
    body(pdf, "Toi la sinh vien nam 4 nganh Khoa hoc may tinh, quan tam den Data Analyst.")
    heading(pdf, "Skills")
    body(pdf, "Python, Pandas, Excel, Power BI, SQL")
    heading(pdf, "Projects")
    body(pdf, "Phan tich du lieu ban hang (2025)\n"
              "- Lam sach du lieu bang Pandas, truc quan hoa bang Power BI\n"
              "- Xay dung dashboard theo doi doanh thu theo khu vuc")
    pdf.output(str(OUT / "cv_missing_sections.pdf"))


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    cv_single_column()
    cv_two_column()
    cv_missing_sections()
    print(f"Da tao 3 CV synthetic trong {OUT}")
