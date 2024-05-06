import socket
import struct
import os
from ansible.module_utils.basic import AnsibleModule

def recv_fd(sock):
    """ Receive a single file descriptor. """
    fds = []
    msg, ancdata, flags, addr = sock.recvmsg(1, socket.CMSG_SPACE(struct.calcsize('i')))
    for cmsg_level, cmsg_type, cmsg_data in ancdata:
        if cmsg_level == socket.SOL_SOCKET and cmsg_type == socket.SCM_RIGHTS:
            fds.extend(struct.unpack('i' * (len(cmsg_data) // struct.calcsize('i')), cmsg_data))
    return fds[0] if fds else None

def response_handler(sock, body, status, content_type):
    fd = recv_fd(sock)
    if fd is not None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, fileno=fd) as client_socket:
            response_body = body
            response_headers = (
                f"HTTP/1.1 {status}\r\n"
                "Content-Type: {content_type}\r\n"
                f"Content-Length: {len(response_body)}\r\n"
                "\r\n"
            )
            response = response_headers + response_body
            client_socket.sendall(response.encode())

def main():

    module_args = dict(
        body=dict(type='str', required=True),
        status=dict(type='str', required=True),
        content_type=dict(type='str', required=False, default='text/plain')
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server_path = "/tmp/ansible_http.sock"
    if os.path.exists(server_path):
        os.unlink(server_path)
    server_socket.bind(server_path)
    server_socket.listen(1)
    while True:
        conn, _ = server_socket.accept()
        with conn:
            response_handler(conn, module.params['body'], module.params['status'], module.params['content_type'])
            break
    server_socket.close()

    module.exit_json(changed=True)

if __name__ == '__main__':
    main()
