from flask import Flask, render_template, request, url_for, redirect
import socket
import json
import hashlib
import struct

app = Flask(__name__)
PACKET_SALT = b"A8!nChS9"
HOST = "localhost" # -> (@TODO) server IP
PORT = 12001

''' Function '''
def gen_packet(ddict):
    header = b""
    header += hashlib.md5(ddict.encode()+PACKET_SALT).digest()[:8]
    header += struct.pack("<I", len(ddict))
    return header + ddict.encode()

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    print(request.form)
    if 'source_code' not in request.form:
        return redirect(url_for('index'))
    # MYSQL QUERY -> time limit, memory limit
    
    Create_Dict = {}
    Create_Dict["LANG"] = request.form['LANG']
    Create_Dict["SOURCE_CODE"] = request.form['source_code'].replace("\r\n", "\n")

    Create_Dict["PROBLEM_ID"] = int(request.form['problem_id'])
    Create_Dict["TIME_LIMIT"] = 1        # LOOKUP DB
    Create_Dict["MEMORY_LIMIT"] = 1000      # LOOKUP DB
    Create_Dict["TMP_FILE_NAME"] = hashlib.md5(Create_Dict["SOURCE_CODE"].encode()).hexdigest()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.send(gen_packet(json.dumps(Create_Dict)))

        # Checking Protocol
        Protocol_Header = sock.recv(12)

        """
        hex(struct.unpack("<I", b"\x34\x12\x00\x00")[0])
        >>> '0x1234'
        """
        
        print("protocol :", Protocol_Header)
        SFOJ_CRC, Dic_len = Protocol_Header[:8], struct.unpack("<I", Protocol_Header[8:])[0]
        Dic = sock.recv(Dic_len)

        if SFOJ_CRC != hashlib.md5(Dic + PACKET_SALT).digest()[:8]:
            sock.send(gen_packet(json.dumps({}))) # empty json
            sock.close()
            return 'Error'

        Dic = json.loads(Dic)
        
        print(Dic)
        result=json.loads(Dic['STATUS'])
        print(type(result))
        sock.close()

    if Create_Dict["LANG"] == 'CXX':
        l = "cpp"
    elif Create_Dict["LANG"] == 'C':
        l = "c"

    # return 'You entered: {}'.format(Dic)
    return render_template('form.html', submit=1, code=Create_Dict["SOURCE_CODE"],result=result['RESULT'], code_language=l)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=False)