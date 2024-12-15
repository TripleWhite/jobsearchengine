from app import create_app
import argparse
import logging

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=5001)
    return parser.parse_args()

# 设置详细的日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('flask.app')
logger.setLevel(logging.DEBUG)

app = create_app()

if __name__ == '__main__':
    args = parse_args()
    app.run(debug=True, port=args.port)
