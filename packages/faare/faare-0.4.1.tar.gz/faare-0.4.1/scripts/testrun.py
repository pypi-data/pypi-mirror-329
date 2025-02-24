from faare import Faare
import os

def main():
    ROOT = os.path.dirname(__file__)

    faare = Faare()
    faare.build_render(os.path.join(ROOT, '..', 'tests', 'data', 'OUTCAR'),
                        os.path.join(ROOT, 'manifest.json'))
    faare.execute_render(os.path.join(ROOT, 'manifest.json'),
                            os.path.join(ROOT, 'render.png'),
                            os.path.join(ROOT, 'renderlog.txt'))

if __name__ == '__main__':
    main()
