# bridgepy
[bridgepy](https://pypi.org/project/bridgepy/) is a Python package for playing floating bridge!

[Visit repository on Github](https://github.com/papillonbee/bridgepy)

---

## Game state

The heart of this project is in the game state below

<img src="https://gist.githubusercontent.com/papillonbee/7f512954267c8340eb20b52ef8016ccf/raw/8673f95b534665510e9a286cb3d92d43dc16cb77/bridgepy-game-state.svg">

---
## Quick Guide
```python
from bridgepy.datastore import Datastore
from bridgepy.player import PlayerId, PlayerAction
from bridgepy.game import GameId, Game
from bridgepy.card import Card
from bridgepy.bid import Bid
from bridgepy.bridge import BridgeClient
```

### Step 1: Create your own datastore for `Game` and override `insert`, `update`, `delete`, and `query`
In this example, is a local datastore

```python
class GameLocalDataStore(Datastore[GameId, Game]):

    def __init__(self) -> None:
        self.games: list[Game] = []

    def insert(self, game: Game) -> None:
        i = self.__query_index(game.id)
        if i is not None:
            return
        self.games.append(game)

    def update(self, game: Game) -> None:
        i = self.__query_index(game.id)
        if i is None:
            return
        self.games = self.games[:i] + [game] + self.games[i+1:]

    def delete(self, id: GameId) -> None:
        i = self.__query_index(id)
        if i is None:
            return
        self.games = self.games[:i] + self.games[i+1:]

    def query(self, id: GameId) -> Game | None:
        i = self.__query_index(id)
        if i is None:
            return None
        return self.games[i]

    def __query_index(self, id: GameId) -> int | None:
        for i in range(len(self.games)):
            if self.games[i].id == id:
                return i
        return None
```
### Step 2: Inject your game datastore to bridge client
In this example, is injecting the local datastore to the bridge client

```python
game_datastore = GameLocalDataStore()
client = BridgeClient(game_datastore)
```

### Step 3: Let 1 player create a game, and let 3 other players join the game

```python
game_id = GameId("1")
player_id1 = PlayerId("111")
player_id2 = PlayerId("222")
player_id3 = PlayerId("333")
player_id4 = PlayerId("444")

client.create_game(player_id1, game_id)
client.join_game(player_id2, game_id)
client.join_game(player_id3, game_id)
client.join_game(player_id4, game_id)
```

### Step 4: Let players bid, choose partner, and trick

```python
player_id = player_id2 # replace with player_id1, player_id2, player_id3, player_id4
# player polls for their game snapshot (maybe every 5 seconds)
snapshot = client.view_game(player_id, game_id)
print(snapshot)
if snapshot.player_action == PlayerAction.VIEW:
    # player keeps polling for their game snapshot
    print("view")
if snapshot.player_action == PlayerAction.BID:
    print("bid turn")
    bid_input = input() # 1C for 1 club, 2NT for 2 no trump, None for pass
    bid = None if bid_input == "" else Bid.from_string(bid_input)
    client.bid(player_id, game_id, bid)
if snapshot.player_action == PlayerAction.CHOOSE_PARTNER:
    print("choose partner")
    partner_input = input() # AC for ace club, 2H for 2 heart, 10S for 10 spade
    client.choose_partner(player_id, game_id, Card.from_string(partner_input))
if snapshot.player_action == PlayerAction.TRICK:
    print("trick turn")
    trick_input = input() # AC for ace club, 2H for 2 heart, 10S for 10 spade
    client.trick(player_id, game_id, Card.from_string(trick_input))
if snapshot.player_action is None:
    # player stops polling for their game snapshot
    print("ended")
```
