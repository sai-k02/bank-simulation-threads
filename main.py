import threading
import random
import time
from queue import Queue

'''
BANK SIMULATION USING THREADS

TELLER THREAD:

CUSTOMER THREAD:

TRANSACTIONS:
    - WITHDRAW
        - MUST GET PERMISSION FROM MANAGER (BLOCK THREAD FOR 5 to 30ms)
    - DEPOSIT ()
VAULT: ONLY TWO TELLERS ARE ALLOWED INSIDE AT ANY ONE TIME

'''


# DEFINE SHARED RESOURCES USING SEMAPHORES
vaultSemaphore = threading.Semaphore(2)
managerSemaphore = threading.Semaphore(1)
tellerSemaphore = threading.Semaphore(3)

bankDoorSemaphore = threading.Semaphore(2)

customerWait = threading.Semaphore(1)

# DEFINE TELLER ID DICTIONARY
TELLER_ID = {
    3: 1,
    2: 2,
    1: 1
}

# VARIABLES USED FOR THE COMMUNICATION BETWEEN TELLER AND CUSTOMER AND MANAGER
sharingData = Queue()


def teller(id):
    while (True):
        customerID = sharingData.get()
        print("Teller %s is serving Customer %s." %
              (id, customerID))

        transactionType = sharingData.get()
        print("Teller %s is handling %s." %
              (id, transactionType))
        # HANDLE TRANSACTION
        print(customerWait._value, "from teller")

        customerWait.acquire()
        # WITHDRAW
        if transactionType == "withdrawl":
            managerSemaphore.acquire()
            print("Teller %s is asking manager." %
                  (id))
            # SLEEP FOR RANDOM TIME BETWEEN 5 to 3ms (mimic manager response time)
            time.sleep(random.randrange(5, 30)/1000)
            # RELEASE THE MANAGER RESOURCE
            managerSemaphore.release()

        # GO TO THE VAULT AKA SAFE
        print("Teller %s is walking to the vault" % id)
        vaultSemaphore.acquire()

        # PERFORM TASK
        print("Teller is physically performing task.")
        time.sleep(random.randrange(10, 50)/1000)

        # COME BACK FROM VAULT
        vaultSemaphore.release()

        # LET CUSTOMER KNOW WE ARE DONE WITH TRANSACTION
        print("Teller %s is finished handling %s." %
              (id, transactionType))

        customerWait.release()


def customer(id):
    # DEFINE TRANSACTION
    transactionType = random.choice(["deposit", "withdrawal"])

    # INITIAL MESSAGE FROM CUSTOMER
    print("Customer %s is going to the bank." % id)

    # GO INSIDE DOOR
    bankDoorSemaphore.acquire()
    bankDoorSemaphore.release()

    # SHOW THAT THE CUSTOMER IS WAITING IN LINE
    print("Customer %s is waiting in line." % id)

    # ENVOKE BANK DUTIES
    # FINDING THE CORRECT TELLER TO COMMUNICATE BETWEEN VIA SEMAPHORE
    print("Customer %s is selecting a teller." % id)
    tellerSemaphore.acquire()
    tellerID = TELLER_ID[tellerSemaphore._value+1]
    print("Customer %s goes to Teller %s." % (id, tellerID))
    sharingData.put(id)
    print("Customer %s introduces itself to Teller %s." % (id, tellerID))

    print("Customer %s asks for a %s transaction." % (id, transactionType))
    sharingData.put(transactionType)

    # CUSTOMER WILL WAIT WHILE TRYING TO ACQUIRE THE CUSTOMERWAIT SEMAPHORE
    print("Customer %s is waiting." %
          (id))
    # WAIT ... TELLER SHOULD HAVE ACQUIRED BEFORE (DOESN'T WORK)
    customerWait.acquire()

    # OUTPUT CUSTOMER IS DONE
    print("Customer %s is done with his %s transaction." %
          (id, transactionType))

    # GIVE 1 BACK TO CUSTOMER WAIT
    customerWait.release()

    # GIVE BACK A TELLER
    tellerSemaphore.release()


# MAIN RESPONSIBLE FOR HANDLE BANK SIMULATION
def main():

    # CREATE THREE TELLERS
    for i in range(3):
        threading.Thread(target=teller, args=(i+1,)).start()

    # CREATE 50 CUSTOMER THREADS
    for i in range(50):
        customerThread = threading.Thread(target=customer, args=(i+1,))
        customerThread.start()


print("The bank has opened up for the day.")
main()
print("The bank has closed for the day.")
