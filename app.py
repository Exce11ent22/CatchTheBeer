from game import Game
import cv2 as cv
import numpy as np


def threshold_function(g, fg):
    if 1 in g.field:
        i = g.field.index(1)
        w = 0
        for line in fg[:128, 128 * i:128 + 128 * i]:
            w += sum(line)
        if w > 300000:
            return True
        return False


def draw_beer(g, im):
    global beer
    if 1 in g.field:
        i = g.field.index(1)
        roi = im[:128, 128 * i:128 * (i + 1)]

        img2gray = cv.cvtColor(beer, cv.COLOR_BGR2GRAY)
        _ret, mask = cv.threshold(img2gray, 20, 255, cv.THRESH_BINARY)
        mask_inv = cv.bitwise_not(mask)

        im_bg = cv.bitwise_and(roi, roi, mask=mask_inv)
        im_fg = cv.bitwise_and(beer, beer, mask=mask)

        dst = cv.add(im_bg, im_fg)
        im[:128, 128 * i:128 * (i + 1)] = dst


if __name__ == '__main__':
    game = Game()
    capture = cv.VideoCapture(0)
    back_sub = cv.createBackgroundSubtractorMOG2()
    beer = cv.imread('beer.png')

    while True:
        ret, img = capture.read()
        fg_mask = back_sub.apply(img)
        game.refresh()
        draw_beer(game, img)
        if threshold_function(game, fg_mask):
            game.collect()

        img = img[:, ::-1, :]
        img = np.array(img)
        if game.loses != 4:
            cv.putText(img, f'Collected: {game.collected}', (0, 160), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
            cv.putText(img, f'Loses: {game.loses}', (0, 200), cv.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0))
            cv.putText(img, f'time of collect: {game.collect_time}', (440, 160), cv.FONT_HERSHEY_DUPLEX, 0.5, (0, 0, 255))
        if game.loses == 3:
            cv.putText(img, 'GAME OVER', (50, 300), cv.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255))
            cv.putText(img, f'RECORD {game.record}', (0, 460), cv.FONT_HERSHEY_DUPLEX, 2, (0, 255, 0))
            cv.putText(img, f'BEST TIME: {game.best_time}', (0, 410), cv.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))

        # if you want to see foreground mask:
        # cv.imshow('Foreground mask', fg_mask)
        cv.imshow('Original', img)

        k = cv.waitKey(15) & 0xFF
        if k == 27:
            break

        r = cv.waitKey(15) & 0xFF
        if r == ord('r'):
            game.restart()

    capture.release()
    cv.destroyAllWindows()
