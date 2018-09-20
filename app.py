from flask import Flask, request, send_file, make_response
from gevent import monkey, pywsgi
from draw_qr import create_qr
import os
import io


monkey.patch_all()
app = Flask(__name__)


@app.route('/qr', methods=['POST'])
def redemption():
    if request.is_json:
        content = request.get_json()

        if content['key'] == 'hold my beer':

            if 'from_hex_color' in content:
                from_hex_color = content['from_hex_color']
            else:
                if 'to_hex_color' in content:
                    from_hex_color = content['to_hex_color']
                else:
                    from_hex_color = '#000000'

            if 'to_hex_color' in content:
                to_hex_color = content['to_hex_color']
            else:
                if 'from_hex_color' in content:
                    to_hex_color = content['from_hex_color']
                else:
                    to_hex_color = '#000000'

            if 'x_pos' in content:
                x_pos = content['x_pos']
            else:
                x_pos = 0.5

            if 'y_pos' in content:
                y_pos = content['y_pos']
            else:
                y_pos = 0.5

            # print(from_hex_color, to_hex_color, x_pos, y_pos)

            qr = create_qr(content['data'], gradient_pos=(x_pos, y_pos), from_hex_color=from_hex_color, to_hex_color=to_hex_color)

            qr_filename = '/var/www/qr/qr_images/' + request.remote_addr + ".jpg"
            qr_filename = os.path.abspath(qr_filename)
            qr.save(qr_filename, 'JPEG')

            with open(qr_filename, 'rb') as bites:
                return send_file(
                    io.BytesIO(bites.read()),
                    attachment_filename='qr.jpg',
                    mimetype='image/jpg'
                )
        else:
            result = "Key: %s is not correct" % content['key']
            return '{"code": -1, "result": "%s"}' % result
    else:
        return '{"code": -2, "result": "JSON"}'


if __name__ == '__main__':
    host_ip = '127.0.0.1'
    print('Serving on %s ...' % host_ip)
    server = pywsgi.WSGIServer((host_ip, 8088), app)
    server.serve_forever()
