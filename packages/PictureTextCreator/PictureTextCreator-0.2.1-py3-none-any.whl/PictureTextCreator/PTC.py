from PIL import Image, ImageFont, ImageDraw
import textwrap

def GetPictureWithText(templatePath, textCordinate, textToAdd , fontPath, outputPath, textColor = (0,0,0), backgroundColor = (255,255,255), fontSize = 45, textWrapValue = 39):

    TEXTSIZE = fontSize

    templateTopImg = Image.open(templatePath)
    templateBotImg = Image.open(templatePath)

    templateTopImg = GetCroppedImage(templateTopImg,textCordinate)
    templateBotImg = GetCroppedImage(templateBotImg,textCordinate, False)

    textLines = textwrap.wrap(textToAdd,textWrapValue)

    #final image height = top template height + bot template height + textsize * lines
    topImgWidth, topImgHeight = templateTopImg.size
    botImgWidth, botImgHeight = templateBotImg.size
    finalImageHeight = (TEXTSIZE * len(textLines)) + topImgHeight + botImgHeight

    finalImage = Image.new("RGBA",(topImgWidth, finalImageHeight))

    editImage = ImageDraw.Draw(finalImage)
    editImage.rectangle([(0,topImgHeight),(topImgWidth,topImgHeight + (TEXTSIZE * len(textLines)))],fill=backgroundColor)
    index = 0
    for line in textLines:
        imageText = ImageFont.truetype(fontPath,TEXTSIZE)
        editImage.text((42, topImgHeight + (index * TEXTSIZE)),line, textColor ,imageText)
        index += 1


    finalImage.paste(templateTopImg,(0,0))
    finalImage.paste(templateBotImg,(0, finalImageHeight - botImgHeight))
    finalImage.save(outputPath)


def GetCroppedImage(imageToCrop, cropLineHeight, isTop = True):
    imgWidth, imgHeight = imageToCrop.size
    
    if isTop == True:
        cropFromBottom =  imgHeight - cropLineHeight
        # left top right bottom
        croppedImage = imageToCrop.crop((0,0,imgWidth,imgHeight - cropFromBottom))
        return croppedImage
    else:
        cropFromTop = imgHeight - (imgHeight - cropLineHeight)
        croppedImage = imageToCrop.crop((0,cropFromTop,imgWidth,imgHeight))
        return croppedImage

