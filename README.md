# 📡 ARP Handling in SDN Networks

## 🧠 Project Overview

This project demonstrates how **Address Resolution Protocol (ARP)** works in a **Software Defined Networking (SDN)** environment using **Mininet** and the **POX controller**.

Instead of traditional network switches handling ARP, the **SDN controller intercepts ARP requests and generates replies**, enabling centralized control over host discovery.

---

## 🎯 Objectives

* Intercept ARP requests at the SDN controller
* Maintain an IP → MAC mapping table
* Generate ARP replies dynamically
* Flood unknown ARP requests when needed
* Enable communication between hosts in a Mininet topology

---

## 🏗️ Project Structure

```
sdn-arp/
│
├── pox/
│   └── arp_handler.py        # SDN controller logic (ARP handling)
│
├── topology/
│   └── topo.py               # Mininet topology (hosts + switch)
│
└── README.md
```

---

## ⚙️ Requirements

Make sure you have:

* Ubuntu / WSL (Linux environment)
* Python 3.9 (or compatible with POX)
* Mininet
* Open vSwitch
* POX controller

---

## 🚀 How to Run the Project

### 🖥️ Terminal 1 — Start the POX Controller

```bash
cd pox
python3.9 pox.py log.level --DEBUG arp_handler
```

👉 This starts the SDN controller and loads the ARP handler module.

---

### 🖧 Terminal 2 — Start Mininet

```bash
sudo mn -c
sudo python3 ~/sdn-arp/topology/topo.py
```

👉 This:

* Clears old Mininet state
* Launches the custom topology
* Connects hosts to a single switch controlled by POX

---

### 💻 Inside Mininet CLI

Once Mininet starts, run:

```bash
mininet> h1 arping h2
```

---

## 🔄 What Happens Internally

1. `h1` sends an ARP request ("Who has h2?")
2. The switch forwards it to the SDN controller
3. The controller (`arp_handler.py`) receives the packet
4. It:

   * Learns IP → MAC mapping
   * Generates ARP reply if destination is known
   * Otherwise floods the request
5. `h2` responds and communication is established

---

## 🧩 Key Concepts Used

* Software Defined Networking (SDN)
* POX Controller event handling
* OpenFlow packet processing
* ARP request/reply mechanism
* Mininet network emulation

---

## 📌 Important Notes

* This project forces **OpenFlow 1.0 compatibility**
* MAC addresses are manually assigned in topology
* Controller maintains a dynamic ARP table
* Designed for learning SDN packet flow, not production use

---

## 🧪 Example Output

```
ARP Request: Who has 10.0.0.2? Tell 10.0.0.1
ARP Reply sent: 10.0.0.2 is at 00:00:00:00:00:02
```

---

## 📚 Learning Outcome

After completing this project, you will understand:

* How ARP works at packet level
* How SDN controllers intercept traffic
* How switches interact with controllers
* How host discovery works in virtual networks

---

## 👨‍💻 Author

SDN ARP Learning Project using Mininet + POX Controller
