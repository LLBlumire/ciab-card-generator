from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import copy
import pytoml as toml
import sys
import textwrap

# CARD_TEMPLATE_REGIONS
money_startx = 25
money_starty = 25
money_lenx = 275
money_leny = 60
prod_startx = 319
prod_starty = 25
prod_lenx = 278
prod_leny = 60
name_startx = 25
name_starty = 105
name_lenx = 572
name_leny = 106
flav_startx = 25
flav_starty = 229
flav_lenx = 572
flav_leny = 626

# RENDER_CONFIG
font_size = 40

# BUILD OPTS
# BITMASK
#  1 = Generate Globals
#  2 = Generate Research
#  4 = Generate Development
#  8 = Generate Testing
# 16 = Generate Maintenence
# 31 = Generate All
build_level = 31

def draw_centered(content, template, font, startx, starty, lenx, leny, cid):
    template = template.convert("RGBA")
    text = Image.new('RGBA', template.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(text)

    (cx, _) = draw.multiline_textsize('m', font=font, spacing=0)
    content = '\n'.join(textwrap.wrap(content, width=lenx//cx))

    (dx, dy) = draw.multiline_textsize(content, font=font, spacing=5)

    if dy > leny:
        print("WARNING: Card {} Overdlowing Y Boundry".format(cid))
    if dx > lenx:
        print("WARNING: Card {} Overdlowing X Boundry".format(cid))

    startx = startx + (lenx/2) - (dx/2)
    starty = starty + (leny/2) - (dy/2)

    draw.text((startx, starty), content, font=font, fill=(0, 0, 0, 255), align='center')
    out = Image.alpha_composite(template, text)
    return out

def draw_card_name(name, template, font, cid):
    return draw_centered(name, template, font, name_startx, name_starty, name_lenx, name_leny, cid)

def draw_card_money(money, template, font, cid):
    return draw_centered(money, template, font, money_startx, money_starty, money_lenx, money_leny, cid)

def draw_card_prod(prod, template, font, cid):
    return draw_centered(prod, template, font, prod_startx, prod_starty, prod_lenx, prod_leny, cid)

def draw_card_flav(flav, template, font, cid):
    return draw_centered(flav, template, font, flav_startx, flav_starty, flav_lenx, flav_leny, cid)


def draw_card(card, flav, template, font, cid):
    template = draw_card_name(card["name"], template, font, cid)
    template = draw_card_flav(flav, template, font, cid)
    try:
        template = draw_card_money(str(card["money_cost"]), template, font, cid)
    except KeyError:
        pass
    try:
        template = draw_card_prod(str(card["productivity_cost"]), template, font, cid)
    except KeyError:
        pass

    return template

with open("build/flav.toml") as flav:
    cards = toml.load(flav)

development = Image.open("build/development.png")
maintenance = Image.open("build/maintenance.png")
research = Image.open("build/research.png")
testing = Image.open("build/testing.png")

font = ImageFont.truetype("build/font.ttf", font_size)

cardcount = 0

if build_level & 1 != 0:
    for card in cards["global"]:
        for flav in card["flavours"]:
            draw_card(card, flav, development, font, cardcount).save('build/output/{}.png'.format(cardcount))
            cardcount += 1
            draw_card(card, flav, maintenance, font, cardcount).save('build/output/{}.png'.format(cardcount))
            cardcount += 1
            draw_card(card, flav, research, font, cardcount).save('build/output/{}.png'.format(cardcount))
            cardcount += 1
            draw_card(card, flav, testing, font, cardcount).save('build/output/{}.png'.format(cardcount))
            cardcount += 1

if build_level & 2 != 0:
    for card in cards["Research"]:
        for flav in card["flavours"]:
            draw_card(card, flav, research, font, cardcount).save('build/output/{}.png'.format(cardcount))
            cardcount += 1

if build_level & 4 != 0:
    for card in cards["Development"]:
        for flav in card["flavours"]:
            draw_card(card, flav, development, font, cardcount).save('build/output/{}.png'.format(cardcount))
            cardcount += 1

if build_level & 8 != 0:
    for card in cards["Testing"]:
        for flav in card["flavours"]:
            draw_card(card, flav, testing, font, cardcount).save('build/output/{}.png'.format(cardcount))
            cardcount += 1

if build_level & 16 != 0:
    for card in cards["Maintenance"]:
        for flav in card["flavours"]:
            draw_card(card, flav, maintenance, font, cardcount).save('build/output/{}.png'.format(cardcount))
            cardcount += 1

