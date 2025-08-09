#  Virtual Chappathi Maker

A fun, interactive 3D simulation of making chappathis (Indian flatbread) in a virtual kitchen, built with **Three.js**. Knead, divide, roll, and cook chappathis using simple keyboard and mouse controls.

---

##  Features

- **Interactive 3D Environment** – A fully rendered kitchen scene provides an immersive backdrop for your culinary creations.
- **Realistic Physics (Simplified)** – Watch the main dough ball jiggle as you knead it.
- **Step-by-Step Process** – Follow the real-life process of making chappathis:
  1. Knead the main dough.
  2. Divide it into smaller portions.
  3. Roll each portion into a flat chappathi.
  4. Cook the chappathi, watching it puff up and change color.
- **Object Interaction** – Click and drag the dough balls to move them around the countertop.
- **Dynamic Stacking** – Cooked chappathis are automatically stacked in a casserole dish.

---

##  Controls

| Action         | Control                              |
| -------------- | ------------------------------------ |
| **Rotate View** | Click & Drag Mouse                   |
| **Move Dough**  | Click & Drag any dough ball           |
| **Divide Dough**| Quick-click the main dough            |
| **Knead**       | Hold `W`                              |
| **Roll**        | Hover a small ball + Hold `A`         |
| **Spread**      | Hover a chappathi + Hold `D`          |
| **Cook**        | Hover a chappathi + Hold `S`          |

---

##  How to Run

Because this project uses JavaScript modules, you need to run it from a local web server.

### Option 1: Using VS Code Live Server (Easiest)
1. Save the project code as `index.html`.
2. Install the **Live Server** extension in VS Code.
3. Right-click `index.html` and select **"Open with Live Server"**.

### Option 2: Using Python's HTTP Server
1. Save the project code as `index.html`.
2. Open a terminal in the project directory.
3. Run the command:
   ```bash
   python -m http.server

