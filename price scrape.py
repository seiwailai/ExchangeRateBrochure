import bs4, requests, re, datetime, os
from PIL import Image, ImageDraw, ImageFont

CNYMYR = "https://www.klmoneychanger.com//forex.php?n=CNY&d=Chinese+Yuan&q="
parentDir = "C:\\Users\\Asus\\Desktop\\Alipay Topup\\Flyers"
startingSpread = 1.075

def scrapePrice(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, "lxml")
    showratebuy = soup.find("table", id="showratebuy")
    showratesell = soup.find("table", id="showratesell")
    sellPrice = showratebuy.find("tr", attrs={'data-target':'#b_CNYMaxMoneyMidValleyMegamall'}).find_next_sibling().find("span").text
    buyPrice = showratesell.find("tr", attrs={'data-target':'#s_CNYMaxMoneyMidValleyMegamall'}).find_next_sibling().find("span").text
    priceRegex = re.compile(r"\d+\.+\d+")
    sellPriceMatch = round(float(priceRegex.findall(sellPrice)[0]),2)
    buyPriceMatch = round(100/float(priceRegex.findall(buyPrice)[0]), 2)
    return sellPriceMatch, buyPriceMatch

def generateRateList(url, startingSpread):
    myrPriceList = [100, 200, 500]
    sellPrice, buyPrice = scrapePrice(url)
    strings = '\n'
    spread = startingSpread
    for i in range(len(myrPriceList)):
        nominalRate = buyPrice/spread
        if i == 0:
            strings += f"RM 1 to RM {myrPriceList[i]-0.01} @ CNY{round(nominalRate,3)}/1MYR \n\n\n"
        else:
            strings += f"RM {myrPriceList[i-1]} to RM {myrPriceList[i]-0.01} @ CNY{round(nominalRate,3)}/1MYR \n\n\n"
        spread = spread - 0.01 - (0.005 * (i+1))
    nominalRate = buyPrice/spread
    strings += f"RM {myrPriceList[-1]} and above @ CNY{round(nominalRate, 3)}/1MYR \n\n\n"
    return strings

def mergeFlyer(url, startingSpread, parentDir):
    now = datetime.datetime.now()
    date = f'{now.day}/{now.month}/{now.year}'
    image = Image.open('flyer sample.png')
    imageWidth, imageHeight = image.size
    draw = ImageDraw.Draw(image)
    string = generateRateList(url, startingSpread)
    pos_date = imageWidth/2.3, imageHeight/2.7
    font_date = ImageFont.truetype("arial.ttf", 35)
    pos_price = imageWidth/4, imageHeight/2.5
    font_price = ImageFont.truetype("arial.ttf", 40)
    draw.text(pos_price, string, 'black', font=font_price)
    draw.text(pos_date, date, 'black', font=font_date)
    path = parentDir + f"\\{now.year}\\{now.month}"
    os.makedirs(path, exist_ok=True)
    image.save(f'{path}/{now.day}.png')

mergeFlyer(CNYMYR, startingSpread, parentDir)
