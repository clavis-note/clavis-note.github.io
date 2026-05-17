"""
架空在留カード画像ジェネレータ (デモモード用)

使い方:
    python3 _zairyu_generator.py

DC001〜DC008 の架空在留カード画像を assets/demo-samples/ に出力する。

設計方針:
- 本物そっくりにしない (法務省ロゴ・公印は省略、SAMPLE透かしを全面に)
- ポイポイ式OCRが各項目を読み取れる情報密度は確保
- 顔写真は赤バンド付き「SAMPLE PHOTO」シルエット
- 下部に「これはデモ用の架空サンプルです」明示
- データは demo.html の DEMO_DATA と整合させる

依存: Pillow, IPAGothic フォント (Linux標準)
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_PATH = "/usr/share/fonts/opentype/ipafont-gothic/ipag.ttf"

# Canvas (在留カード比率 85.6:54 ≈ 1.585:1)
W, H = 1500, 946
BG = (252, 250, 245)


def F(size):
    return ImageFont.truetype(FONT_PATH, size)


def draw_card(data, out_filename):
    """1枚の在留カード画像を生成して保存。

    data: dict with keys
        card_number, name, dob_jp, dob_en, sex_jp, sex_en,
        nationality_jp, nationality_en, address,
        status_jp, status_en, period_jp, period_en, expiry_jp,
        permission_type, permission_date
    """
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    # 外枠
    draw.rectangle([20, 20, W - 20, H - 20], outline=(170, 160, 140), width=4)

    # 上部タイトル帯
    draw.rectangle([20, 20, W - 20, 150], fill=(244, 240, 230), outline=(170, 160, 140), width=4)
    draw.text((50, 45), "在留カード", fill=(40, 40, 40), font=F(50))
    draw.text((50, 110), "RESIDENCE CARD", fill=(110, 110, 110), font=F(20))

    # 右上の番号
    no_x = W - 510
    draw.text((no_x, 38), "番号 / Number", fill=(110, 110, 110), font=F(16))
    draw.text((no_x, 60), data["card_number"], fill=(30, 30, 30), font=F(46))

    # 顔写真エリア
    photo_x, photo_y = 60, 200
    photo_w, photo_h = 230, 290
    draw.rectangle(
        [photo_x, photo_y, photo_x + photo_w, photo_y + photo_h],
        outline=(140, 140, 140), width=2, fill=(228, 228, 228),
    )
    # シルエット
    hcx = photo_x + photo_w // 2
    hcy = photo_y + photo_h // 3 + 10
    draw.ellipse([hcx - 42, hcy - 42, hcx + 42, hcy + 42], fill=(170, 170, 170))
    shoulder_y = photo_y + photo_h // 2 + 35
    draw.ellipse([hcx - 85, shoulder_y, hcx + 85, shoulder_y + 160], fill=(170, 170, 170))
    # SAMPLE PHOTO バンド
    band_y = photo_y + photo_h - 50
    draw.rectangle(
        [photo_x + 5, band_y, photo_x + photo_w - 5, band_y + 36],
        fill=(220, 70, 70),
    )
    draw.text((photo_x + 38, band_y + 6), "SAMPLE PHOTO", fill=(255, 255, 255), font=F(20))

    # 各項目
    info_x = photo_x + photo_w + 50
    label_w = 280
    y = 200

    def put(label_jp, label_en, value, big=False):
        nonlocal y
        draw.text((info_x, y), label_jp, fill=(95, 95, 95), font=F(16))
        draw.text((info_x, y + 20), label_en, fill=(140, 140, 140), font=F(11))
        fs = 30 if big else 24
        draw.text((info_x + label_w, y + (3 if big else 7)), value, fill=(20, 20, 20), font=F(fs))
        y += 56

    put("氏名", "NAME", data["name"], big=True)
    put("生年月日", "DATE OF BIRTH", f"{data['dob_jp']}  /  {data['dob_en']}")
    put("性別", "SEX", f"{data['sex_jp']}  /  {data['sex_en']}")
    put("国籍・地域", "NATIONALITY / REGION", f"{data['nationality_jp']}  /  {data['nationality_en']}")
    put("住居地", "ADDRESS", data["address"])
    put("在留資格", "STATUS", f"{data['status_jp']}  /  {data['status_en']}")
    put("在留期間(満了日)", "PERIOD OF STAY (DATE OF EXPIRATION)",
        f"{data['period_jp']}  /  {data['period_en']}  ({data['expiry_jp']})")
    put("許可の種類", "TYPE OF PERMISSION", data["permission_type"])
    put("許可年月日", "DATE OF PERMISSION", data["permission_date"])

    # 透かし
    overlay = Image.new("RGBA", (W, H), (255, 255, 255, 0))
    od = ImageDraw.Draw(overlay)
    sf = F(150)
    for x in range(-100, W + 200, 580):
        for ya in range(-100, H + 200, 360):
            od.text((x, ya), "SAMPLE", fill=(210, 60, 60, 38), font=sf)
    overlay = overlay.rotate(-22, resample=Image.BICUBIC, expand=False)
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # 下部の注意書き帯
    draw.rectangle(
        [20, H - 95, W - 20, H - 20],
        fill=(252, 235, 235),
        outline=(180, 70, 70),
        width=3,
    )
    draw.text(
        (50, H - 80),
        "⚠ これはデモ用の架空サンプルです。実在の人物・公的書類を模したものではありません。",
        fill=(140, 30, 30),
        font=F(20),
    )
    draw.text(
        (50, H - 48),
        "SAMPLE FOR DEMO ONLY  -  This is NOT an actual residence card. "
        "All information is fictitious.",
        fill=(160, 80, 80),
        font=F(15),
    )

    # 出力
    out = os.path.join(OUT_DIR, out_filename)
    img.save(out, "PNG", optimize=True)
    print(f"Saved: {out_filename}  ({os.path.getsize(out):,} bytes)")


# ----- DC001 ~ DC008 のデータ定義 -----
# demo.html の DEMO_DATA と整合させる
DC001 = {
    "card_number":   "AB12345678CD",
    "name":          "SAPKOTA DIPAK",
    "dob_jp":        "1992年4月15日",
    "dob_en":        "15 APR 1992",
    "sex_jp":        "男",
    "sex_en":        "M",
    "nationality_jp":"ネパール",
    "nationality_en":"NEPAL",
    "address":       "東京都立川市高松町1-2-3 サンプル荘101",
    "status_jp":     "技能",
    "status_en":     "SKILLED LABOR",
    "period_jp":     "3年",
    "period_en":     "3 YEARS",
    "expiry_jp":     "2026年6月13日",
    "permission_type":"在留期間更新許可",
    "permission_date":"2023年6月13日",
}

# DC002〜DC008 は試作版OK後に追記する

if __name__ == "__main__":
    draw_card(DC001, "zairyu_DC001.png")
