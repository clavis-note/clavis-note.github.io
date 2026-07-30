#!/usr/bin/env python3
"""撮影・スクショ用ダミーデータJSONを生成する。

Clavis Note 本番の「JSONから復元」からインポートできる形式で出力する。
在留期限アラート（45日前・15日前など）が常に画になるよう、日付は
実行日基準の相対日付で焼き込む。撮影前に再実行すると日付が今日基準に
リフレッシュされる。

使い方（リポジトリルートで）:
    python demo-data/generate_demo_data.py

出力: demo-data/clavis-demo-data.json

注意:
  - 全データは架空。実在の人物・企業とは無関係（THAPA RAM は従来からの
    撮影用ダミー人物名）。
  - templates / fee_master / docTypes は含めない → インポート時に
    migrateData がデフォルトを補完する（構造変更への追従も同機構に任せる）。
"""
import json
from datetime import date, timedelta
from pathlib import Path

OUT = Path(__file__).resolve().parent / "clavis-demo-data.json"
TODAY = date.today()


def ymd(offset_days):
    return (TODAY + timedelta(days=offset_days)).isoformat()


def client(**kw):
    """クライアント1件。app.html の handleAddClient のフィールド構成に合わせる。"""
    base = {
        "client_id": "", "client_type": "immigration",
        "name_roman": "", "name_kana": "", "nationality": "", "dob": "", "gender": "",
        "passport_number": "", "passport_expiry": "", "entry_date": "",
        "residence_card": "", "residence_status": "", "residence_expiry": "", "residence_period": "",
        "phone": "", "email": "", "company_name": "", "store": "", "work_start_date": "",
        "notes": "", "address": "", "postal_code": "", "occupation": "", "home_residence": "",
        "dependent_of": None, "client_status": "active", "relationship": None, "school_name": None,
        "coe_phase": False, "coe_category": None,
        "photo": None, "archived": False,
        "salary_history": [], "work_history": [],
        "drive_path": "", "drive_url": "",
        "education_school": "", "education_date": "",
        "custody_status": None, "custody_received_date": "", "custody_return_due": "",
        "custody_reason": "", "custody_returned_date": "", "custody_history": [],
    }
    base.update(kw)
    return base


def case(**kw):
    """案件1件。新規案件登録＋migrateData 補完後のフィールド構成に合わせる。"""
    base = {
        "case_id": "", "no": 0, "category": "国際", "client_id": "", "template_id": None,
        "case_title": "", "status": "相談中",
        "accepted_date": "", "applied_date": None, "result_date": None,
        "receipt_number": "", "result": "", "new_card": "", "period": "", "next_renewal": "",
        "fee": 0, "paid": 0,
        "applicant": "", "applicant_id": "", "requester": "", "requester_id": "",
        "notes": "", "official_req_no": "",
        "invoice_no": "", "invoice_date": "", "due_date": "", "bill_to": "",
        "docs": [], "hearing_items": [], "additional_requests": [],
        "contacts": [], "comm_log": [], "payment_logs": [], "doc_count": "",
    }
    base.update(kw)
    return base


def doc(i, name, status="未取得", group=None):
    return {"id": f"d{i}", "name": name, "group": group, "status": status}


def payment(**kw):
    """請求1件。payments[] のフィールド構成に合わせる。"""
    base = {
        "payment_id": "", "case_ids": [], "client_ids": [],
        "bill_type": "individual", "bill_to_name": "", "honorific": "様",
        "tax_mode": "tax_incl",
        "invoice_number": "", "invoice_date": "", "due_date": "",
        "items": [], "expenses": [], "payments_history": [],
        "notes": "", "is_prospect": False, "prospect_archived": False,
    }
    base.update(kw)
    return base


DATA = {
    "office": {
        "name": "サンプル国際行政書士事務所",
        "representative": "鍵谷 誠",
        "postal": "190-0012",
        "address1": "東京都立川市曙町",
        "address2": "2-34-5 クラヴィスビル3F",
        "phone": "042-000-0000",
        "email": "info@sample-gyosei.example",
        "bank_lines": ["サンプル銀行 立川支店 普通 1234567", "口座名義 サンプル国際行政書士事務所"],
        "credential_expiry": ymd(300),
        "license_key": "",
        "onboarding_completed": True,
        "tour_completed": True,
    },
    "clients": [
        client(
            client_id="D001", name_roman="THAPA RAM", name_kana="タパ ラム",
            nationality="ネパール", dob="1992-04-15", gender="男",
            passport_number="PA1234567", passport_expiry=ymd(720), entry_date="2018-06-10",
            residence_card="AB12345678CD", residence_status="技能", residence_expiry=ymd(45),
            residence_period="3年", phone="080-0000-1001", email="ram@example.com",
            company_name="株式会社サンプル飲食", store="立川店", work_start_date="2018-07-01",
            address="東京都立川市", postal_code="190-0011", occupation="調理師",
            education_school="カトマンズ調理専門学校", education_date="2016-03-15",
            work_history=[{"id": "WH001", "company_name": "株式会社サンプル飲食", "country": "日本",
                           "start_date": "2018-07-01", "end_date": "", "auto": True, "store": "立川店"}],
            salary_history=[
                {"id": "S001", "work_id": "WH001", "effective_date": "2018-07-01",
                 "monthly_salary": 210000, "hourly_wage": 1211, "weekly_hours": 40,
                 "employment_type": "正社員", "pref": "東京都", "min_wage_check": True},
                {"id": "S002", "work_id": "WH001", "effective_date": "2025-04-01",
                 "monthly_salary": 255000, "hourly_wage": 1471, "weekly_hours": 40,
                 "employment_type": "正社員", "pref": "東京都", "min_wage_check": True},
            ],
        ),
        client(
            client_id="D002", name_roman="SITA THAPA", name_kana="シタ タパ",
            nationality="ネパール", dob="1995-08-22", gender="女",
            passport_number="PA7654321", passport_expiry=ymd(900), entry_date="2019-12-15",
            residence_card="EF98765432GH", residence_status="家族滞在", residence_expiry=ymd(45),
            residence_period="3年", phone="080-0000-1002",
            notes="D001 THAPA RAM の配偶者", address="東京都立川市", postal_code="190-0011",
            dependent_of="D001", relationship="妻",
        ),
        client(
            client_id="D003", name_roman="NGUYEN VAN MINH", name_kana="グエン ヴァン ミン",
            nationality="ベトナム", dob="1990-12-03", gender="男",
            passport_number="PB2345678", passport_expiry=ymd(540), entry_date="2017-04-01",
            residence_card="IJ23456789KL", residence_status="技術・人文知識・国際業務",
            residence_expiry=ymd(120), residence_period="5年",
            phone="080-0000-1003", email="minh@example.com",
            company_name="株式会社サンプルIT", work_start_date="2017-04-15",
            address="東京都新宿区", postal_code="160-0023", occupation="システムエンジニア",
            education_school="ハノイ工科大学", education_date="2015-06-30",
            work_history=[{"id": "WH002", "company_name": "株式会社サンプルIT", "country": "日本",
                           "start_date": "2017-04-15", "end_date": "", "auto": True, "store": ""}],
            salary_history=[
                {"id": "S003", "work_id": "WH002", "effective_date": "2017-04-15",
                 "monthly_salary": 280000, "hourly_wage": 1615, "weekly_hours": 40,
                 "employment_type": "正社員", "pref": "東京都", "min_wage_check": True},
            ],
        ),
        client(
            client_id="D004", name_roman="LI MING", name_kana="リ ミン",
            nationality="中国", dob="1988-03-18", gender="男",
            passport_number="PC3456789", passport_expiry=ymd(1080), entry_date="2015-08-20",
            residence_card="MN34567890OP", residence_status="永住者", residence_expiry=ymd(2190),
            residence_period="無期限", phone="080-0000-1004", email="li.ming@example.com",
            company_name="株式会社サンプル商事", store="本店", work_start_date="2015-09-01",
            notes="永住許可取得済み", address="千葉県市川市", postal_code="272-0021",
            occupation="貿易事務", education_school="北京大学", education_date="2012-07-10",
            work_history=[{"id": "WH003", "company_name": "株式会社サンプル商事", "country": "日本",
                           "start_date": "2015-09-01", "end_date": "", "auto": True, "store": "本店"}],
        ),
        client(
            client_id="D005", name_roman="SANTOS MARIA", name_kana="サントス マリア",
            nationality="フィリピン", dob="1993-09-05", gender="女",
            passport_number="PD4567890", passport_expiry=ymd(450), entry_date="2020-02-14",
            residence_card="QR45678901ST", residence_status="特定技能1号", residence_expiry=ymd(15),
            residence_period="1年", phone="080-0000-1005",
            company_name="株式会社サンプル介護", store="立川施設", work_start_date="2020-03-01",
            notes="⚠️在留期限間近（要更新申請）", address="東京都立川市", postal_code="190-0001",
            occupation="介護職員", education_school="マニラ看護学校", education_date="2014-04-20",
            work_history=[{"id": "WH004", "company_name": "株式会社サンプル介護", "country": "日本",
                           "start_date": "2020-03-01", "end_date": "", "auto": True, "store": "立川施設"}],
        ),
        client(
            client_id="D006", name_roman="KIM JISOO", name_kana="キム ジス",
            nationality="韓国", dob="1996-11-30", gender="女",
            passport_number="PE5678901", passport_expiry=ymd(300), entry_date="2022-09-01",
            residence_card="UV56789012WX", residence_status="留学", residence_expiry=ymd(200),
            residence_period="2年3月", phone="080-0000-1006", email="jisoo@example.com",
            school_name="日本語学校サンプルアカデミー", client_status="student",
            notes="卒業後の就職（技人国への変更）希望", address="東京都豊島区", postal_code="170-0013",
            education_school="ソウル大学", education_date="2022-02-28",
        ),
        client(
            client_id="D007", name_roman="GURUNG BIKASH", name_kana="グルン ビカス",
            nationality="ネパール", dob="1994-01-25", gender="男",
            passport_number="PF6789012", passport_expiry=ymd(1400),
            coe_phase=True, coe_category="work", client_status="incoming",
            company_name="株式会社サンプル飲食", store="八王子店",
            notes="COE申請中（来日前）。現地はポカラ在住。", home_residence="ネパール・ポカラ",
            education_school="ポカラ調理技術学校", education_date="2014-11-30",
        ),
        client(
            client_id="D008", name_roman="SHARMA HARI", name_kana="シャルマ ハリ",
            nationality="ネパール", dob="1985-07-12", gender="男",
            passport_number="PG7890123", passport_expiry="2024-06-30", entry_date="2010-04-20",
            residence_card="YZ67890123AB", residence_status="技能", residence_expiry="2024-08-15",
            residence_period="3年", client_status="returned", notes="2024年に帰国済み",
        ),
        client(
            client_id="D009", client_type="general",
            phone="03-0000-2001", email="info@sample-corp.example",
            company_name="株式会社サンプルコーポレーション",
            notes="会社設立コンサル案件", address="東京都港区", postal_code="107-0052",
        ),
    ],
    "cases": [
        case(
            case_id="DC001", no=1, client_id="D001", template_id="T03",
            case_category="更新", residence_status="技能",
            case_title="技能（調理）継続更新", status="書類収集中",
            accepted_date=ymd(-25), fee=55000,
            applicant="THAPA RAM", applicant_id="D001",
            requester="株式会社サンプル飲食",
            notes="在留期限まで45日。妻（家族滞在）と同時申請予定。",
            docs=[
                doc(1, "在留カード（表裏コピー）", "取得済"),
                doc(2, "パスポート（身分事項・査証ページコピー）", "取得済"),
                doc(3, "写真（縦4cm×横3cm）", "未取得"),
                doc(4, "課税証明書（市区町村発行）", "未取得"),
                doc(5, "法定調書合計表", "未取得"),
            ],
            hearing_items=[
                {"id": "h1", "type": "text", "label": "最終学歴の学校名", "link": "education_school",
                 "answer": "カトマンズ調理専門学校", "date": ""},
                {"id": "h2", "type": "date", "label": "卒業年月日", "link": "education_date",
                 "answer": "", "date": "2016-03-15"},
            ],
            contacts=[{"id": "ct1", "name": "田中 花子", "role": "勤務先担当", "phone": "042-000-0001",
                       "email": "tanaka@sample-foods.example", "note": "書類回収の窓口"}],
            comm_log=[
                {"id": "cl1", "date": ymd(-25), "contact_name": "本人", "method": "対面",
                 "content": "更新のご依頼。妻の分も同時に受任。"},
                {"id": "cl2", "date": ymd(-10), "contact_name": "田中 花子", "method": "メール",
                 "content": "法定調書合計表の準備を依頼。"},
            ],
        ),
        case(
            case_id="DC002", no=2, client_id="D003", template_id="T21",
            case_category="更新", residence_status="技術・人文知識・国際業務",
            case_title="技術・人文知識・国際業務 継続更新", status="申請中",
            accepted_date=ymd(-40), applied_date=ymd(-5),
            receipt_number="東オン認12345678", fee=60500,
            applicant="NGUYEN VAN MINH", applicant_id="D003",
            requester="株式会社サンプルIT",
            docs=[doc(i + 1, n, "提出済") for i, n in enumerate([
                "在留カード（表裏コピー）", "パスポート", "写真（縦4cm×横3cm）",
                "住民票（世帯全員）", "課税証明書", "納税証明書", "源泉徴収票", "在職証明書",
            ])],
        ),
        case(
            case_id="DC003", no=3, client_id="D005", template_id=None,
            case_category="更新", residence_status="特定技能1号",
            case_title="特定技能1号 在留期間更新", status="相談中",
            accepted_date=ymd(-7), fee=66000,
            applicant="SANTOS MARIA", applicant_id="D005",
            requester="株式会社サンプル介護",
            notes="在留期限まで15日。至急対応。",
        ),
        case(
            case_id="DC004", no=4, client_id="D004", template_id="T30",
            case_category="永住", residence_status="永住者",
            case_title="永住許可申請", status="許可",
            accepted_date=ymd(-380), applied_date=ymd(-200), result_date=ymd(-30),
            receipt_number="東オン認99999999", result="許可", new_card="YES", period="無期限",
            fee=150000, applicant="LI MING", applicant_id="D004", requester="LI MING",
            notes="無事許可。おめでとうございます！",
        ),
        case(
            case_id="DC005", no=5, client_id="D002", template_id="T05",
            case_category="更新", residence_status="家族滞在",
            case_title="家族滞在 初回担当更新", status="書類収集中",
            accepted_date=ymd(-20), fee=44000,
            applicant="SITA THAPA", applicant_id="D002", requester="THAPA RAM",
            notes="D001（夫）と同時申請",
            docs=[
                doc(1, "写真（縦4cm×横3cm）※16歳以上", "取得済"),
                doc(2, "在留カード（本人）", "取得済"),
                doc(3, "パスポート（本人）", "取得済"),
                doc(4, "在留カード（扶養者）", "取得済"),
                doc(5, "パスポート（扶養者）", "取得済"),
                doc(6, "婚姻証明書", "未取得", "続柄証明"),
                doc(7, "出生証明書", "不要", "続柄証明"),
                doc(8, "扶養者の在職証明書", "未取得"),
                doc(9, "扶養者の課税証明書", "未取得"),
            ],
        ),
        case(
            case_id="DC006", no=6, client_id="D007", template_id="T01",
            case_category="認定（COE）", residence_status="技能",
            case_title="技能（調理）COE", status="申請中",
            accepted_date=ymd(-60), applied_date=ymd(-14),
            receipt_number="東オン認55555555", fee=110000,
            applicant="GURUNG BIKASH", applicant_id="D007",
            requester="株式会社サンプル飲食",
            notes="八王子店の新規招へい。結果待ち。",
            docs=[doc(1, "写真（縦4cm×横3cm）", "提出済"), doc(2, "パスポート", "提出済"),
                  doc(3, "職務経歴書", "提出済"), doc(4, "雇用契約書", "提出済", "招へい企業資料"),
                  doc(5, "登記事項証明書", "提出済", "招へい企業資料")],
        ),
        case(
            case_id="DG001", no=7, category="会社設立", case_type="general", client_id="D009",
            case_title="株式会社設立手続", status="作業中",
            accepted_date=ymd(-15), fee=100000,
            applicant="株式会社サンプルコーポレーション",
            requester="株式会社サンプルコーポレーション",
            notes="定款作成中",
            comm_log=[{"id": "cl3", "date": ymd(-15), "contact_name": "佐藤 次郎", "method": "対面",
                       "content": "設立スケジュールの打ち合わせ。"}],
        ),
    ],
    "payments": [
        # まとめ請求（夫婦同時申請）: 明細の applicant で案件按分。案件側 fee と一致させてある
        payment(
            payment_id="PM001", case_ids=["DC001", "DC005"], client_ids=["D001", "D002"],
            bill_to_name="THAPA RAM", honorific="様",
            invoice_number="INV-2026-0031", invoice_date=ymd(-8), due_date=ymd(22),
            items=[
                {"id": "i1", "name": "在留期間更新許可申請（技能）", "unit_price": 55000,
                 "quantity": 1, "applicant": "THAPA RAM"},
                {"id": "i2", "name": "在留期間更新許可申請（家族滞在）", "unit_price": 44000,
                 "quantity": 1, "applicant": "SITA THAPA"},
            ],
        ),
        payment(
            payment_id="PM002", case_ids=["DC002"], client_ids=["D003"],
            bill_type="company", bill_to_name="株式会社サンプルIT", honorific="御中",
            tax_mode="tax_excl",
            invoice_number="INV-2026-0024", invoice_date=ymd(-35), due_date=ymd(-5),
            items=[{"id": "i1", "name": "在留期間更新許可申請（技人国）", "unit_price": 55000, "quantity": 1}],
            payments_history=[{"id": "h1", "date": ymd(-12), "amount": 60500, "method": "振込", "note": ""}],
        ),
        payment(
            payment_id="PM003", case_ids=["DC004"], client_ids=["D004"],
            bill_to_name="LI MING", honorific="様",
            invoice_number="INV-2026-0008", invoice_date=ymd(-28), due_date=ymd(2),
            items=[{"id": "i1", "name": "永住許可申請 報酬", "unit_price": 150000, "quantity": 1}],
            expenses=[{"id": "e1", "date": ymd(-200), "name": "収入印紙代（立替）", "amount": 8000, "billable": True}],
            payments_history=[{"id": "h1", "date": ymd(-20), "amount": 158000, "method": "振込", "note": ""}],
        ),
        payment(
            payment_id="PM004", case_ids=["DC006"], client_ids=["D007"],
            bill_type="company", bill_to_name="株式会社サンプル飲食", honorific="御中",
            invoice_number="INV-2026-0019", invoice_date=ymd(-45), due_date=ymd(-15),
            items=[{"id": "i1", "name": "在留資格認定証明書交付申請（技能）", "unit_price": 110000, "quantity": 1}],
            payments_history=[{"id": "h1", "date": ymd(-40), "amount": 55000, "method": "振込", "note": "着手金"}],
        ),
        payment(
            payment_id="PM005", case_ids=["DG001"], client_ids=["D009"],
            bill_type="company", bill_to_name="株式会社サンプルコーポレーション", honorific="御中",
            invoice_number="INV-2026-0027", invoice_date=ymd(-12), due_date=ymd(18),
            items=[{"id": "i1", "name": "株式会社設立手続 報酬", "unit_price": 100000, "quantity": 1}],
            expenses=[{"id": "e1", "date": ymd(-10), "name": "定款認証手数料（立替）", "amount": 52000, "billable": True}],
            payments_history=[{"id": "h1", "date": ymd(-10), "amount": 50000, "method": "振込", "note": "着手金"}],
        ),
        # 見込案件（見積書）
        payment(
            payment_id="PROSP001", is_prospect=True,
            bill_type="company", bill_to_name="株式会社サンプル物流", honorific="御中",
            subject="特定技能1号 COE申請（3名）",
            estimate_number="EST-2026-0012", estimate_date=ymd(-3), estimate_valid=ymd(27),
            estimate_note="ご発注後、着手金として50%を申し受けます。",
            items=[{"id": "i1", "name": "在留資格認定証明書交付申請（特定技能1号）", "unit_price": 82500, "quantity": 3}],
        ),
    ],
    "companies": [
        {"company_id": "CO001", "name": "株式会社サンプル飲食", "short_name": "サンプル飲食", "pref": "東京都", "status": "active"},
        {"company_id": "CO002", "name": "株式会社サンプルIT", "short_name": "サンプルIT", "pref": "東京都", "status": "active"},
        {"company_id": "CO003", "name": "株式会社サンプル商事", "short_name": "サンプル商事", "pref": "千葉県", "status": "active"},
        {"company_id": "CO004", "name": "株式会社サンプル介護", "short_name": "サンプル介護", "pref": "東京都", "status": "active"},
        {"company_id": "CO005", "name": "株式会社サンプルコーポレーション", "short_name": "サンプル法人", "pref": "東京都", "status": "active"},
    ],
    "links": [
        {"id": "L1", "name": "オンライン申請システム", "url": "https://www.ras-immi.moj.go.jp/", "icon": "🖥️", "category": "申請"},
        {"id": "L2", "name": "出入国在留管理庁", "url": "https://www.moj.go.jp/isa/", "icon": "🏛️", "category": "入管"},
        {"id": "L3", "name": "在留カード番号確認", "url": "https://lapse-immi.moj.go.jp/ZEC/appl/e0/ZEC2/pages/FZECST011.aspx", "icon": "💳", "category": "入管"},
        {"id": "L5", "name": "東京都最低賃金", "url": "https://jsite.mhlw.go.jp/tokyo-roudoukyoku/news_topics/chingin_toukei/chingin.html", "icon": "📊", "category": "参考"},
        {"id": "L6", "name": "日本行政書士会連合会", "url": "https://www.gyosei.or.jp/", "icon": "📜", "category": "参考"},
    ],
}


def main():
    OUT.write_text(json.dumps(DATA, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} (基準日: {TODAY.isoformat()})")
    print(f"  clients: {len(DATA['clients'])} / cases: {len(DATA['cases'])} / payments: {len(DATA['payments'])}")


if __name__ == "__main__":
    main()
