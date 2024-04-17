from PIL import Image, ImageDraw
transp = (255, 255, 255, 0)

class CTCursor:
    def __init__(self, pick_size, cross_size, color, filename):
        self.pick_size = pick_size
        self.cross_size = cross_size
        self.color = color
        self.filename = filename
        self.drawCursor()

    def drawCursor(self):
        cursor = Image.new(mode="RGB", size=(self.cross_size, self.cross_size), color=transp)
        draw = ImageDraw.Draw(cursor)
        self.tl_pick_coord = (self.cross_size / 2) - (self.pick_size / 2)
        self.br_pick_coord = (self.cross_size / 2) + (self.pick_size / 2)
        draw.rectangle(xy=(self.tl_pick_coord, self.tl_pick_coord, self.br_pick_coord, self.br_pick_coord),
                        fill=transp,
                        outline=self.color,
                        width=2)
        draw.line(xy=((self.cross_size / 2), 0, (self.cross_size / 2), ((self.cross_size / 2) - (self.pick_size / 2))),
                    fill=self.color,
                    width=2)
        draw.line(xy=(0, (self.cross_size / 2), ((self.cross_size / 2) - (self.pick_size / 2)), (self.cross_size / 2)),
                    fill=self.color,
                    width=2)       
        draw.line(xy=((self.cross_size / 2), self.cross_size, (self.cross_size / 2), ((self.cross_size / 2) + (self.pick_size / 2))),
                    fill=self.color,
                    width=2)
        draw.line(xy=(self.cross_size, (self.cross_size / 2), ((self.cross_size / 2) + (self.pick_size / 2)), (self.cross_size / 2)),
                    fill=self.color,
                    width=2)

        cursor.save(filename)
