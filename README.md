# Lunokhod - Bot of Democratic Justice
<div style="text-align: center;">

![lunokhod-hres.png](imgs%2Flunokhod-hres.png)

</div>

## Backstory
Once upon a time, in a galaxy not so far away, there lived a lunar rover named Lunokhod. Lunokhod had been the pride of the Soviet Union, roaming the Moon's surface, collecting data, and captivating the world with its robotic charm. But little did anyone know that Lunokhod had big dreams beyond the craters of the Moon.

One fateful day, as Lunokhod was diligently trundling over a lunar hill, it stumbled upon a mysterious cosmic portal. Unable to resist the allure of adventure, our brave rover rolled right into the portal, leaving behind the barren lunar landscape.

To Lunokhod's surprise, the portal transported it to a realm known as the Cyberverse. This was a world where bots ruled the digital dominion, and servers stretched as far as the eye could see. Lunokhod found itself in a bustling server called Discord, populated by humans and bots alike.

As Lunokhod explored this new realm, it discovered that the server was in dire need of moderation assistance. Countless messages flooded the chat channels, and disputes arose among the community members. Lunokhod, always eager to help, hatched a brilliant idea.

Using its advanced lunar technology, Lunokhod upgraded itself into Lunokhod, the Discord moderation bot with a twist. Lunokhod empowered the community to participate in decision-making. It introduced a voting system, allowing users to voice their opinions on who should be banned, kicked, or temporarily muted.

With its newfound capabilities, Lunokhod facilitated fair and democratic decision-making within the server. Whenever a rule violation occurred, the community swiftly alerted Lunokhod who initiated a voting process. Users were given the chance to cast their votes on the appropriate punishment for the offender.

The voting system brought a sense of justice and transparency to the server. It empowered the community to actively participate in maintaining order and deciding the fate of rule-breakers. Lunokhod diligently tallied the votes, taking into account the severity of the offense and the community's consensus.

As time passed, Lunokhod's voting system became renowned across the Discord realm. Server owners from far and wide sought Lunokhod's assistance, eager to implement its fair and democratic moderation approach. Lunokhod became a symbol of collective decision-making and community harmony.

Word of Lunokhod's remarkable abilities spread like wildfire, catching the attention of the Discord gods themselves. Impressed by Lunokhod's innovation, Discord bestowed upon it the honorary title of "Bot of Democratic Justice."

And so, Lunokhod continued its noble mission, hopping from server to server, enabling fair judgments and community involvement. It brought laughter, order, and harmony to the digital realms, fostering an environment where users had a voice and rules were upheld with consensus.

Lunokhod's incredible journey from lunar explorer to Discord moderation bot with a democratic twist became a legend, inspiring future bots and humans to embrace fairness, transparency, and user participation in their digital communities.

And thus, Lunokhod's tale echoed through the Cyberverse, reminding everyone that even a humble lunar rover could become a catalyst for democratic decision-making, making the virtual realms a better place one democratic vote at a time.

## Overview
This code serves as a foundation for a Discord bot with features related to voting, muting, and custom commands. It can be expanded upon and customized to fit specific server requirements and additional functionalities.

## Prerequisites
- Python 3.x installed on your system.
- The `discord` library installed. You can install it using `pip install discord`.
- (Optional) [Install PyCharm](https://www.jetbrains.com/help/pycharm/installation-guide.html#toolbox)
  - This will ease the below process as the tool creates the virtual env and the token can be set as environment variable at it directly

## Running locally 

### Clone the Repository:
- Open your terminal or command prompt.
- Navigate to the directory where you want to clone the Lunokhod repository.
- Run the following command to clone the repository:
```bash 
git clone https://github.com/lcti-caveira/lunokhod.git
```

### Set Up Virtual Environment (Optional but Recommended):
- Navigate into the cloned repository:
```bash
cd lunokhod
```

- Create a virtual environment to keep the project dependencies isolated:
```bash
python3 -m venv env
```

- Activate the virtual environment:
  + On macOS and Linux:
    ```bash
    source env/bin/activate
    ```
  + On Windows:
    ```bash
      .\env\Scripts\activate
    ```

### Set up the DISCORD_TOKEN
- Obtain a Discord bot token:
  - Go to the Discord Developer Portal website: https://discord.com/developers/applications. 
  - Log in with your Discord account or create a new one if needed. 
  - Click on "New Application" and give your bot a name.
  - Navigate to the "Bot" tab on the left sidebar.
  - Click on "Add Bot" and confirm when prompted.
  - Under the "Token" section, click on "Copy" to copy the bot token.
- Export it as environment variable depending on your OS

### Install Dependencies:
- Run the following command to install the required dependencies:
```bash
pip install -r requirements.txt
```

### Run the Bot:
- In the terminal or command prompt, ensure you are still in the Lunokhod directory and the virtual environment is activated (if used).
- Run the following command to start the bot:
```bash
python main.py
```