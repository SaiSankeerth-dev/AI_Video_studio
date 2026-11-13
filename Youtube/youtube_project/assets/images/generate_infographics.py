from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

out_dir = r"E:\AI_Videos\Youtube\youtube_project\assets\images"
os.makedirs(out_dir, exist_ok=True)

W, H = 1920, 1080

def create_base_canvas(color=(15, 17, 21)):
    im = Image.new("RGBA", (W, H), color + (255,))
    draw = ImageDraw.Draw(im)
    # subtle forensic grid
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(25, 29, 36, 120), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(25, 29, 36, 120), width=1)
    return im, draw

# SHOT 02: Six glowing booster boxes in acrylic grid
def make_shot_02():
    im, draw = create_base_canvas((12, 14, 18))
    # Title overlay
    draw.text((100, 80), "EVIDENCE ARTIFACT // WOTC 1999 BASE SET", fill=(0, 229, 255), font=None)
    draw.text((100, 110), "6x 1ST EDITION BOOSTER BOXES (SPECULATIVE RECONSTRUCTION)", fill=(245, 239, 235), font=None)
    
    # 6 boxes in 3x2 grid
    box_w, box_h = 420, 320
    start_x, start_y = 240, 240
    for row in range(2):
        for col in range(3):
            bx = start_x + col * (box_w + 80)
            by = start_y + row * (box_h + 80)
            # Box outer shadow
            draw.rectangle([bx-10, by-10, bx+box_w+10, by+box_h+10], fill=(0, 0, 0, 180))
            # Box body
            draw.rectangle([bx, by, bx+box_w, by+box_h], fill=(26, 32, 44, 255), outline=(0, 229, 255, 200), width=2)
            # Box artwork placeholder
            draw.rectangle([bx+20, by+20, bx+box_w-20, by+box_h-70], fill=(18, 22, 28, 255))
            draw.text((bx+40, by+80), "POKEMON TCG 1999", fill=(255, 159, 28), font=None)
            draw.text((bx+40, by+120), "1ST EDITION BASE SET", fill=(245, 239, 235), font=None)
            draw.text((bx+40, by+160), "36 BOOSTER PACKS // SEALED", fill=(0, 229, 255), font=None)
            # Certification label
            draw.rectangle([bx+20, by+box_h-50, bx+box_w-20, by+box_h-20], fill=(0, 229, 255, 30), outline=(0, 229, 255, 150))
            draw.text((bx+30, by+box_h-45), f"BOX SERIAL #WOTC-99-0{row*3+col+1} // VERIFIED VAULT", fill=(0, 229, 255), font=None)
    
    # Corner forensic reticles
    draw.text((1600, 1000), "STATUS: UNVERIFIED INTERNAL ASSET", fill=(255, 159, 28), font=None)
    im.save(os.path.join(out_dir, "shot-02.png"))
    print("Generated shot-02.png")

# SHOT 05: Archived Canadian eBay Listing UI
def make_shot_05():
    im, draw = create_base_canvas((15, 18, 24))
    # Browser Window Bar
    draw.rectangle([120, 80, 1800, 140], fill=(28, 32, 40, 255))
    draw.ellipse([140, 105, 155, 120], fill=(255, 95, 86))
    draw.ellipse([165, 105, 180, 120], fill=(255, 189, 46))
    draw.ellipse([190, 105, 205, 120], fill=(39, 201, 63))
    draw.rectangle([230, 95, 1780, 130], fill=(18, 20, 26, 255))
    draw.text((250, 105), "https://www.ebay.ca/itm/archived-listing-march-2021-case-base-set", fill=(160, 170, 185), font=None)
    
    # eBay Content Body
    draw.rectangle([120, 140, 1800, 980], fill=(22, 26, 34, 255))
    # Left column: Box photo placeholder
    draw.rectangle([180, 200, 800, 750], fill=(14, 16, 20, 255), outline=(60, 70, 85))
    draw.text((360, 460), "[ARCHIVED AUCTION PHOTO // CARDBOARD CASE]", fill=(120, 130, 145), font=None)
    
    # Right column: Listing Details
    draw.text((860, 200), "VINTAGE POKEMON 1ST EDITION BASE SET CASE - SEALED", fill=(245, 239, 235), font=None)
    draw.text((860, 240), "Winning bid: C $72,500.00 (Approximately $57,800 USD)", fill=(39, 201, 63), font=None)
    draw.text((860, 280), "Ended: Mar 28, 2021 18:42:15 EDT", fill=(160, 170, 185), font=None)
    
    # Seller Box with RED WARNING CALLOUT
    draw.rectangle([860, 360, 1720, 560], fill=(32, 38, 50, 255), outline=(255, 159, 28, 200), width=2)
    draw.text((890, 390), "SELLER INFORMATION // CRITICAL FORENSIC LEAD", fill=(255, 159, 28), font=None)
    # Highlighted username
    draw.rectangle([890, 430, 1400, 490], fill=(255, 159, 28, 40), outline=(255, 159, 28), width=3)
    draw.text((910, 445), "User ID: number1pokemonmaster (0 Feedback)", fill=(255, 220, 100), font=None)
    draw.text((890, 510), "Account Location: Ontario, Canada | Account Age: 4 days before listing", fill=(220, 100, 100), font=None)
    
    # Forensic stamp
    draw.rectangle([860, 640, 1720, 880], fill=(18, 20, 26, 255), outline=(0, 229, 255, 180))
    draw.text((890, 670), "FORENSIC DISCREPANCY NOTE #01:", fill=(0, 229, 255), font=None)
    draw.text((890, 710), "1. Seller changed account username twice during active auction.", fill=(245, 239, 235), font=None)
    draw.text((890, 750), "2. Seller refused in-person pickup or third-party expert inspection.", fill=(245, 239, 235), font=None)
    draw.text((890, 790), "3. Real 6-box 1st Edition case market value: ~$2,500,000 USD.", fill=(255, 95, 86), font=None)
    draw.text((890, 830), "4. Sold for $72,500 (~3% of actual market value).", fill=(255, 95, 86), font=None)
    
    im.save(os.path.join(out_dir, "shot-05.png"))
    print("Generated shot-05.png")

# SHOT 06: Contradictory Provenance Dossier
def make_shot_06():
    im, draw = create_base_canvas((14, 16, 20))
    # Big title
    draw.text((100, 60), "FORENSIC DOSSIER // CONFLICTING ORIGIN ACCOUNTS", fill=(255, 159, 28), font=None)
    
    # Left Card: Story A
    draw.rectangle([120, 140, 920, 940], fill=(24, 28, 36, 255), outline=(220, 60, 60, 200), width=2)
    draw.rectangle([120, 140, 920, 220], fill=(40, 20, 24, 255))
    draw.text((160, 170), "STORY A: CANADIAN ESTATE SALE DISCOVERY", fill=(255, 95, 86), font=None)
    draw.text((160, 260), "SOURCE: Seller's initial email to prospective private buyers", fill=(160, 170, 185), font=None)
    draw.text((160, 320), "\"Found this box cleaning out an old woman's house in rural Ontario.", fill=(245, 239, 235), font=None)
    draw.text((160, 360), "She had no idea what was in it. Selling as-is. Don't know anything", fill=(245, 239, 235), font=None)
    draw.text((160, 400), "about cards, just want quick cash.\"", fill=(245, 239, 235), font=None)
    # Stamp
    draw.rectangle([200, 700, 600, 820], outline=(255, 95, 86), width=4)
    draw.text((230, 745), "CONTRADICTION DETECTED", fill=(255, 95, 86), font=None)
    
    # Right Card: Story B
    draw.rectangle([1000, 140, 1800, 940], fill=(24, 28, 36, 255), outline=(220, 60, 60, 200), width=2)
    draw.rectangle([1000, 140, 1800, 220], fill=(40, 20, 24, 255))
    draw.text((1040, 170), "STORY B: CHILDHOOD BIRTHDAY PRESENT", fill=(255, 95, 86), font=None)
    draw.text((1040, 260), "SOURCE: Seller's eBay direct message inquiry response", fill=(160, 170, 185), font=None)
    draw.text((1040, 320), "\"My uncle bought this case for my 12th birthday in 1999.", fill=(245, 239, 235), font=None)
    draw.text((1040, 360), "I never opened it, it sat in my closet climate controlled attic", fill=(245, 239, 235), font=None)
    draw.text((1040, 400), "for 22 years until I decided to sell it.\"", fill=(245, 239, 235), font=None)
    # Stamp
    draw.rectangle([1080, 700, 1480, 820], outline=(255, 95, 86), width=4)
    draw.text((1110, 745), "CONTRADICTION DETECTED", fill=(255, 95, 86), font=None)
    
    im.save(os.path.join(out_dir, "shot-06.png"))
    print("Generated shot-06.png")

# SHOT 07: 3D Bar Chart - $2.5M vs $72,500
def make_shot_07():
    im, draw = create_base_canvas((10, 12, 16))
    draw.text((100, 60), "THE PARADOX // VALUATION ANOMALY", fill=(255, 159, 28), font=None)
    draw.text((100, 100), "AUTHENTIC MARKET VALUATION VS. SUSPICIOUS SALE PRICE", fill=(160, 170, 185), font=None)
    
    # Ground reflection line
    draw.line([(100, 850), (1820, 850)], fill=(40, 48, 60), width=2)
    
    # Red Bar: $2,500,000 (Height = 650px)
    draw.rectangle([340, 200, 700, 850], fill=(220, 45, 60, 240), outline=(255, 95, 86), width=3)
    # 3D top facet
    draw.polygon([(340, 200), (440, 140), (800, 140), (700, 200)], fill=(255, 95, 86, 255))
    # 3D right facet
    draw.polygon([(700, 200), (800, 140), (800, 790), (700, 850)], fill=(160, 30, 40, 255))
    draw.text((380, 250), "AUTHENTIC 1999 CASE VALUE", fill=(255, 255, 255), font=None)
    draw.text((380, 310), "$2,500,000+", fill=(255, 255, 255), font=None)
    draw.text((380, 370), "($400K+ per box x 6)", fill=(240, 200, 200), font=None)
    
    # Green Bar: $72,500 (Height = 25px)
    draw.rectangle([1120, 825, 1480, 850], fill=(39, 201, 63, 240), outline=(80, 240, 110), width=2)
    draw.polygon([(1120, 825), (1200, 800), (1560, 800), (1480, 825)], fill=(80, 240, 110, 255))
    draw.polygon([(1480, 825), (1560, 800), (1560, 825), (1480, 850)], fill=(25, 140, 45, 255))
    draw.text((1140, 710), "CANADIAN EBAY SALE PRICE", fill=(160, 170, 185), font=None)
    draw.text((1140, 750), "$72,500", fill=(39, 201, 63), font=None)
    draw.text((1140, 780), "(~2.9% of real value)", fill=(255, 95, 86), font=None)
    
    # Giant Question Mark
    draw.text((900, 400), "?", fill=(255, 159, 28, 160), font=None)
    
    im.save(os.path.join(out_dir, "shot-07.png"))
    print("Generated shot-07.png")

# SHOT 08: Isolated Pedestal in Spotlight
def make_shot_08():
    im = Image.new("RGBA", (W, H), (8, 10, 14, 255))
    draw = ImageDraw.Draw(im)
    # Draw soft theatrical spotlight
    for r in range(450, 0, -10):
        alpha = int(25 * (1 - r/450))
        draw.ellipse([W//2 - r, 700 - r//3, W//2 + r, 700 + r//3], fill=(255, 240, 200, alpha))
    # Pedestal
    draw.rectangle([W//2 - 140, 680, W//2 + 140, 950], fill=(22, 26, 32, 255), outline=(45, 52, 64))
    # Cardboard Box on pedestal
    draw.rectangle([W//2 - 180, 480, W//2 + 180, 680], fill=(160, 115, 75, 255), outline=(120, 85, 50), width=3)
    # Tape seam
    draw.rectangle([W//2 - 180, 560, W//2 + 180, 595], fill=(210, 180, 100, 200))
    # Dark silhouettes of people walking away in the background
    draw.text((120, 100), "MARKET VERDICT // ELITE COLLECTORS WALKED AWAY", fill=(255, 159, 28), font=None)
    draw.text((120, 140), "NO MAJOR VINTAGE POKEMON INVESTOR TOUCHED THE AUCTION", fill=(160, 170, 185), font=None)
    im.save(os.path.join(out_dir, "shot-08.png"))
    print("Generated shot-08.png")

# SHOT 09: Speculative Price Escalator Timeline
def make_shot_09():
    im, draw = create_base_canvas((12, 14, 18))
    draw.text((100, 60), "SPECULATIVE CHAIN OF CUSTODY // MARCH - DECEMBER 2021", fill=(0, 229, 255), font=None)
    draw.text((100, 100), "VALUE MULTIPLIED 48X WITHOUT ONCE BREAKING THE SEAL", fill=(255, 159, 28), font=None)
    
    milestones = [
        ("MARCH 2021", "EBAY CANADA", "$72,500", 250, 780),
        ("JUNE 2021", "PRIVATE BROKER A", "$1,200,000", 680, 620),
        ("OCTOBER 2021", "BOLILLO LAJAN SAN", "$2,700,000", 1120, 440),
        ("DECEMBER 2021", "LOGAN PAUL", "$3,500,000", 1560, 240)
    ]
    
    # Connecting ascending staircase line
    pts = [(m[3]+80, m[4]+50) for m in milestones]
    for i in range(len(pts)-1):
        draw.line([pts[i], pts[i+1]], fill=(0, 229, 255, 200), width=4)
        
    for date, owner, price, x, y in milestones:
        # Platform
        draw.rectangle([x-60, y, x+220, y+160], fill=(24, 30, 40, 255), outline=(0, 229, 255, 180), width=2)
        draw.text((x-40, y+20), date, fill=(160, 170, 185), font=None)
        draw.text((x-40, y+55), owner, fill=(245, 239, 235), font=None)
        draw.text((x-40, y+95), price, fill=(255, 159, 28) if "3,500,000" in price else (39, 201, 63), font=None)
        # Small box icon
        draw.rectangle([x+40, y-50, x+120, y], fill=(160, 115, 75), outline=(120, 85, 50))
        
    im.save(os.path.join(out_dir, "shot-09.png"))
    print("Generated shot-09.png")

# SHOT 10: Schrödinger's Box Paradox HUD
def make_shot_10():
    im, draw = create_base_canvas((15, 12, 16))
    # Red glowing laser tripwire along center
    draw.line([(0, H//2), (W, H//2)], fill=(255, 45, 60), width=6)
    
    # Warning HUD Card
    draw.rectangle([W//2 - 450, H//2 - 250, W//2 + 450, H//2 + 250], fill=(24, 16, 20, 240), outline=(255, 45, 60), width=3)
    draw.text((W//2 - 400, H//2 - 200), "THE SCHRÖDINGER'S BOX PARADOX", fill=(255, 95, 86), font=None)
    draw.text((W//2 - 400, H//2 - 140), "CRITICAL VINTAGE COLLECTIBLE MARKET INCENTIVE:", fill=(245, 239, 235), font=None)
    draw.text((W//2 - 400, H//2 - 80), "• SEALED MARKET VALUATION: $3,500,000 USD", fill=(39, 201, 63), font=None)
    draw.text((W//2 - 400, H//2 - 20), "• CUT TAPE TO INSPECT CONTENTS: INSTANT -50% TO -70% PENALTY", fill=(255, 45, 60), font=None)
    draw.text((W//2 - 400, H//2 + 40), "RESULT: NO BUYER OR BROKER DARED TO CUT THE TAPE.", fill=(255, 159, 28), font=None)
    draw.text((W//2 - 400, H//2 + 100), "THE FRAUD WAS PROTECTED ENTIRELY BY MARKET FEAR.", fill=(255, 220, 100), font=None)
    
    im.save(os.path.join(out_dir, "shot-10.png"))
    print("Generated shot-10.png")

# SHOT 12: Barcode Typography Forensic Analysis
def make_shot_12():
    im, draw = create_base_canvas((14, 16, 20))
    draw.text((100, 60), "OPTICAL FORENSICS // THERMAL BARCODE LABEL DISCREPANCY", fill=(0, 229, 255), font=None)
    
    # Mockup of Thermal Shipping Label
    draw.rectangle([300, 160, 1620, 920], fill=(240, 236, 228, 255), outline=(180, 170, 155), width=2)
    draw.text((360, 200), "WIZARDS OF THE COAST - DISTRIBUTION LOGISTICS", fill=(20, 24, 30), font=None)
    draw.text((360, 240), "ITEM: WOC06000 // 1ST EDITION BASE SET BOOSTER CASE (6)", fill=(20, 24, 30), font=None)
    
    # Barcode lines
    for i in range(360, 1560, 14):
        w = 4 if (i // 14) % 3 == 0 else 8
        draw.line([(i, 320), (i, 540)], fill=(10, 12, 16), width=w)
        
    draw.text((750, 560), "*WOC-9901-0842-CA*", fill=(10, 12, 16), font=None)
    
    # Forensic Loupe Overlay (Cyan Reticle)
    cx, cy, rad = 1100, 430, 220
    draw.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], outline=(0, 229, 255), width=4)
    draw.line([(cx-rad-40, cy), (cx+rad+40, cy)], fill=(0, 229, 255), width=2)
    draw.line([(cx, cy-rad-40), (cx, cy+rad+40)], fill=(0, 229, 255), width=2)
    
    # Forensic Callout Note
    draw.rectangle([1180, 680, 1860, 940], fill=(16, 22, 30, 240), outline=(0, 229, 255), width=2)
    draw.text((1210, 710), "FONT ANOMALY DETECTED:", fill=(0, 229, 255), font=None)
    draw.text((1210, 750), "• Modern digital sans-serif kerning", fill=(255, 159, 28), font=None)
    draw.text((1210, 790), "• Not present on 1999 Zebra thermal printers", fill=(245, 239, 235), font=None)
    draw.text((1210, 830), "• Digital vector interpolation proves post-2000 origin", fill=(255, 95, 86), font=None)
    
    im.save(os.path.join(out_dir, "shot-12.png"))
    print("Generated shot-12.png")

# SHOT 13: Chicago Cold Skyline Establishing
def make_shot_13():
    im, draw = create_base_canvas((8, 12, 18))
    # Cold city skyline silhouette
    buildings = [
        (100, 300, 220), (250, 450, 340), (450, 220, 550), (620, 360, 420),
        (800, 180, 600), (1050, 260, 500), (1250, 380, 380), (1450, 200, 560), (1650, 340, 400)
    ]
    for x, w, h in buildings:
        draw.rectangle([x, 900 - h, x + w, 900], fill=(18, 26, 38, 255), outline=(35, 48, 68))
        # Skyscraper windows
        for wx in range(x + 20, x + w - 20, 30):
            for wy in range(900 - h + 30, 880, 40):
                if (wx + wy) % 7 == 0:
                    draw.rectangle([wx, wy, wx+12, wy+18], fill=(255, 220, 120, 180))
    # Fog layer
    draw.rectangle([0, 750, W, 1080], fill=(12, 18, 26, 200))
    draw.text((100, 100), "LOCATION: CHICAGO, ILLINOIS // JANUARY 8, 2022", fill=(0, 229, 255), font=None)
    draw.text((100, 140), "THE CONFRONTATION AT BASEBALL CARD EXCHANGE HEADQUARTERS", fill=(245, 239, 235), font=None)
    im.save(os.path.join(out_dir, "shot-13.png"))
    print("Generated shot-13.png")

# SHOT 15: Puffy Curvy Booster Box Lid
def make_shot_15():
    im, draw = create_base_canvas((16, 18, 22))
    draw.text((100, 60), "PHYSICAL INSPECTION // INTERNAL BOOSTER BOX ANOMALIES", fill=(255, 159, 28), font=None)
    
    # Booster Box Illustration
    draw.rectangle([460, 240, 1460, 840], fill=(32, 40, 54, 255), outline=(255, 95, 86), width=3)
    # Warped lid curvature lines
    draw.arc([460, 180, 1460, 300], start=0, end=180, fill=(255, 95, 86), width=4)
    draw.text((500, 340), "DEFECT 1: WARPED 'PUFFY' LID (INCORRECT INTERNAL VOLUME)", fill=(255, 95, 86), font=None)
    draw.text((500, 420), "DEFECT 2: IRREGULAR NON-FACTORY CRAFT HOT-GLUE SEAMS", fill=(255, 95, 86), font=None)
    draw.text((500, 500), "DEFECT 3: MODERN GLOSS FINISH ON CARDBOARD SUBSTRATE", fill=(255, 95, 86), font=None)
    draw.text((500, 580), "DEFECT 4: MISSING WIZARDS OF THE COAST SECURITY EMBOSSING", fill=(255, 95, 86), font=None)
    
    # Giant Red Warning Stamp
    draw.rectangle([500, 680, 1100, 780], outline=(255, 45, 60), width=4)
    draw.text((540, 715), "AUTHENTICITY FAILURE // RE-SEALED BOX", fill=(255, 45, 60), font=None)
    im.save(os.path.join(out_dir, "shot-15.png"))
    print("Generated shot-15.png")

# SHOT 17: Giant Kinetic Quote "G.I. JOE?!"
def make_shot_17():
    im, draw = create_base_canvas((10, 10, 14))
    # Giant typography
    draw.text((120, 140), "THE MOMENT OF DISCOVERY // LOGAN PAUL LIVE UNBOXING", fill=(255, 159, 28), font=None)
    
    draw.rectangle([120, 260, 1800, 820], fill=(20, 16, 22, 255), outline=(255, 95, 86), width=3)
    draw.text((180, 340), "\"G.I. JOE?!\"", fill=(255, 95, 86), font=None)
    draw.text((180, 480), "\"G.I. JOE?! IT COULD HAVE BEEN ANYTHING ELSE!\"", fill=(245, 239, 235), font=None)
    
    draw.text((180, 640), "CONTENTS: 1991 IMPEL G.I. JOE SERIES 2 WAX PACKS", fill=(0, 229, 255), font=None)
    draw.text((180, 710), "ESTIMATED VALUATION: ~$5 PER PACK // TOTAL PACKS: 216", fill=(160, 170, 185), font=None)
    draw.text((180, 760), "NET FINANCIAL LOSS: $3,498,920 USD", fill=(255, 45, 60), font=None)
    im.save(os.path.join(out_dir, "shot-17.png"))
    print("Generated shot-17.png")

# SHOT 18: Precision Balance Scale Calibrated Weight
def make_shot_18():
    im, draw = create_base_canvas((12, 16, 22))
    draw.text((100, 60), "FORENSIC EXPLANATION // WEIGHT CALIBRATION METHODOLOGY", fill=(0, 229, 255), font=None)
    
    # Scale base
    draw.rectangle([W//2 - 400, 750, W//2 + 400, 850], fill=(30, 36, 46), outline=(0, 229, 255))
    # Digital LED Screen
    draw.rectangle([W//2 - 200, 770, W//2 + 200, 830], fill=(10, 25, 15))
    draw.text((W//2 - 140, 785), "WEIGHT: 380.4g == 380.4g [MATCH]", fill=(39, 201, 63), font=None)
    
    # Balance beam and pans
    draw.line([(W//2, 450), (W//2, 750)], fill=(80, 95, 115), width=8)
    draw.line([(W//2 - 450, 450), (W//2 + 450, 450)], fill=(80, 95, 115), width=8)
    
    # Left Pan (Pokemon Box)
    draw.line([(W//2 - 450, 450), (W//2 - 550, 620)], fill=(60, 75, 95), width=3)
    draw.line([(W//2 - 450, 450), (W//2 - 350, 620)], fill=(60, 75, 95), width=3)
    draw.line([(W//2 - 600, 620), (W//2 - 300, 620)], fill=(0, 229, 255), width=5)
    draw.rectangle([W//2 - 520, 520, W//2 - 380, 620], fill=(26, 32, 44), outline=(0, 229, 255))
    draw.text((W//2 - 510, 560), "POKEMON BOOSTER", fill=(0, 229, 255), font=None)
    
    # Right Pan (G.I. Joe Packs)
    draw.line([(W//2 + 450, 450), (W//2 + 350, 620)], fill=(60, 75, 95), width=3)
    draw.line([(W//2 + 450, 450), (W//2 + 550, 620)], fill=(60, 75, 95), width=3)
    draw.line([(W//2 + 300, 620), (W//2 + 600, 620)], fill=(255, 159, 28), width=5)
    draw.rectangle([W//2 + 380, 520, W//2 + 520, 620], fill=(32, 24, 20), outline=(255, 159, 28))
    draw.text((W//2 + 390, 560), "GI JOE WAX PACKS", fill=(255, 159, 28), font=None)
    
    draw.text((100, 920), "THE CON: 36 wax-paper packs with cardboard insert cards matched the gram weight of 36 foil Pokemon packs within 0.2g.", fill=(245, 239, 235), font=None)
    im.save(os.path.join(out_dir, "shot-18.png"))
    print("Generated shot-18.png")

# SHOT 19: Wire Transfer Refund & Legal Epilogue
def make_shot_19():
    im, draw = create_base_canvas((12, 14, 18))
    draw.text((100, 60), "AFTERMATH // RESOLUTION & RESTITUTION", fill=(39, 201, 63), font=None)
    
    # Wire Transfer Receipt Card
    draw.rectangle([200, 160, 1000, 880], fill=(22, 28, 36, 255), outline=(39, 201, 63), width=2)
    draw.text((250, 210), "WIRE TRANSFER RESTITUTION CONFIRMATION", fill=(39, 201, 63), font=None)
    draw.text((250, 270), "FROM: BOLILLO LAJAN SAN (MATT ALLEN)", fill=(245, 239, 235), font=None)
    draw.text((250, 320), "TO: LOGAN PAUL ENTERPRISES LLC", fill=(245, 239, 235), font=None)
    draw.text((250, 380), "AMOUNT: $3,500,000.00 USD", fill=(39, 201, 63), font=None)
    draw.text((250, 440), "STATUS: FULL REIMBURSEMENT EXECUTED", fill=(39, 201, 63), font=None)
    draw.text((250, 500), "REFERENCE: BBCE SEALED CASE RETRACTION", fill=(160, 170, 185), font=None)
    
    # Legal Statement on right
    draw.rectangle([1060, 160, 1720, 880], fill=(22, 28, 36, 255), outline=(160, 170, 185), width=2)
    draw.text((1100, 210), "BBCE PUBLIC STATEMENT", fill=(255, 159, 28), font=None)
    draw.text((1100, 270), "\"We took a chance authenticating an item", fill=(245, 239, 235), font=None)
    draw.text((1100, 310), "outside our primary sports wheelhouse.", fill=(245, 239, 235), font=None)
    draw.text((1100, 350), "We made an error. We take full responsibility.\"", fill=(245, 239, 235), font=None)
    draw.text((1100, 430), "THE CANADIAN SCAMMER:", fill=(255, 95, 86), font=None)
    draw.text((1100, 470), "Deleted eBay account and vanished.", fill=(255, 95, 86), font=None)
    
    im.save(os.path.join(out_dir, "shot-19.png"))
    print("Generated shot-19.png")

# SHOT 20: Stardust Cosmic Dissolution
def make_shot_20():
    im = Image.new("RGBA", (W, H), (6, 8, 12, 255))
    draw = ImageDraw.Draw(im)
    # Stardust particles
    import random
    random.seed(42)
    for _ in range(800):
        px = random.randint(0, W)
        py = random.randint(0, H)
        size = random.randint(1, 4)
        alpha = random.randint(80, 255)
        gold = random.choice([(255, 215, 0), (255, 159, 28), (255, 240, 180), (0, 229, 255)])
        draw.ellipse([px, py, px+size, py+size], fill=gold + (alpha,))
        
    # Central soft glowing question mark
    draw.text((W//2 - 60, H//2 - 140), "?", fill=(255, 215, 0, 180), font=None)
    draw.text((W//2 - 280, H//2 + 100), "VALUE IS NOT IN THE CARDBOARD.", fill=(245, 239, 235), font=None)
    draw.text((W//2 - 250, H//2 + 150), "IT LIVES IN OUR WILLINGNESS TO BELIEVE.", fill=(255, 159, 28), font=None)
    
    im.save(os.path.join(out_dir, "shot-20.png"))
    print("Generated shot-20.png")

# Generate all
make_shot_02()
make_shot_05()
make_shot_06()
make_shot_07()
make_shot_08()
make_shot_09()
make_shot_10()
make_shot_12()
make_shot_13()
make_shot_15()
make_shot_17()
make_shot_18()
make_shot_19()
make_shot_20()

print("All infographic and procedural image plates generated successfully.")
