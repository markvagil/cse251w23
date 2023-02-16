import multiprocessing
from multiprocessing.connection import PipeConnection


def sender(conn: PipeConnection):
    msgs = ["Hello", ", ", "how ", "are", "you", "?"]

    for msg in msgs:
        conn.send(msg)
    
    conn.send(None)


def another_sender(recevier: PipeConnection, sender: PipeConnection):

    while True:
        msg = recevier.recv()
        sender.send(msg)
        if(msg == None):
            break
        print(f'receiver: message = {msg}')

def receiver(recevier1: PipeConnection, recevier2: PipeConnection):
    
    while True:
        msg = recevier1.recv()
        if(msg == None):
            break
        print(f'another_receiver: message = {msg}')

def main():

    send_conn1, recv_conn1 = multiprocessing.Pipe()
    send_conn2, recv_conn2 = multiprocessing.Pipe()

    p1 = multiprocessing.Process(target=sender, args=(send_conn1,))
    p2 = multiprocessing.Process(target=another_sender, args=(send_conn2,))
    p3 = multiprocessing.Process(target=receiver, args=(recv_conn1, recv_conn2))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()


if __name__ == "__main__":
    main()
