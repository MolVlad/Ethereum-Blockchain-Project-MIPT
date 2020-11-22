pragma solidity ^0.5.0;
pragma experimental ABIEncoderV2;

contract Monopoly
{
	uint8 currentNumberOfPlayers = 0;
	uint8 constant maxNumberOfPlayers = 2;
	uint8 whoseMove = 0;
	bool gameIsActive = false; 
	uint8 constant numberOfStations = 12;

	struct Player
	{
		address addr;
		string name;
		int money;
		uint8 position;
		uint8 movesInPrison;
		bool canBuyStation;
	}

	enum StationCondition { None, Available, Bought }
	struct Station
	{
		StationCondition condition;
		uint8 owner;
        string name;
	}

	mapping (uint => Player) players;
	mapping (uint => Station) stations;

	constructor() public
	{
		// stations corresponding to available stations
		stations[1].condition = StationCondition.Available;
		stations[2].condition = StationCondition.Available;
		stations[5].condition = StationCondition.Available;
		stations[7].condition = StationCondition.Available;
		stations[8].condition = StationCondition.Available;
		stations[11].condition = StationCondition.Available;

		stations[1].name = "Avenue 1";
		stations[2].name = "Avenue 2";
		stations[5].name = "Avenue 3";
		stations[7].name = "Avenue 4";
		stations[8].name = "Avenue 5";
		stations[11].name = "Avenue 6";
	}

	// ------------------------------------------ //
	// ---------| Public functions |------------- //
	// ------------------------------------------ //

	// ---------|  get functions   |------------- //

	function getMaxNumberOfPlayers() public pure returns (uint)
	{
		return maxNumberOfPlayers;
	}

	function getNumberOfStations() public pure returns (uint)
	{
		return numberOfStations;
	}
	
	function getNumberOfPlayers() public view returns (uint)
	{
		return currentNumberOfPlayers;
	}

	function getPlayerByIndex(uint index) public view returns (Player memory)
	{
		return players[index];
	}

	function getStationByIndex(uint index) public view returns (Station memory)
	{
		return stations[index];
	}

	// return number in blockchain base to access your player
	function getNumberOfPlayerByName(string memory name) public view returns (int8)
	{
		for (int8 i=0; uint8(i)<maxNumberOfPlayers; i++)
		{
            if (keccak256(bytes(players[uint8(i)].name)) == keccak256(bytes(name)))
			{
				return i;
			}
		}

		return int8(-1);
	}

	// has the game already started but not finished yet
	function isGameActive() public view returns (bool)
	{
		return gameIsActive;
	}

	// who can make move now? returns player's name
	function getWhoseMove() public view returns (string memory name)
	{
		return players[whoseMove].name;
	}

	// ---------|  action functions   |------------- //

	// enroll the game to play, need to call to start the game
	function enroll(string memory name) public returns (bool)
	{
		// if there are free spaces and player is not yet in game
		if ((currentNumberOfPlayers < maxNumberOfPlayers) && (!isPlayer(msg.sender)))
		{
			players[currentNumberOfPlayers].addr = msg.sender;
			players[currentNumberOfPlayers].money = 200;
			players[currentNumberOfPlayers].name = name;

			currentNumberOfPlayers++;

			if (currentNumberOfPlayers == maxNumberOfPlayers)
			{
				gameIsActive = true;
			}

			return true;
		}
		else
		{
			return false;
		}
	}

	// make a move if it is ours
	function makeMove() public returns (bool)
	{
		// if user is appropriate
		if ((msg.sender == players[whoseMove].addr) && !players[whoseMove].canBuyStation && gameIsActive)
		{
			// generate random number for dice
			uint256 r = timestampHash();
			uint8 dice = uint8(r % 6 + 1);

			// handle case when player is in prison
			if (players[whoseMove].movesInPrison > 0)
			{
				players[whoseMove].movesInPrison--;
			}
			else
			{
				players[whoseMove].position = uint8((players[whoseMove].position + dice) % numberOfStations);
			}

			// emit event for returning dice value
			emit moveIsMade(players[whoseMove].name, dice);

			// handle cases with stations
			handleStations();

			// if the station can be bought, return actionRequired=true 
			if ((stations[players[whoseMove].position].condition == StationCondition.Available) && (players[whoseMove].money >= 200))
			{
				players[whoseMove].canBuyStation = true;
			}
			// otherwise pass the move
			else
			{
				whoseMove = ((whoseMove) + 1) % maxNumberOfPlayers;
			}

			return true;
		}
		else
		{
			return false;
		}
	}

	// buy station if now we can
	function buyStation(bool decision) public returns (bool)
	{
		if ((msg.sender == players[whoseMove].addr) && players[whoseMove].canBuyStation && gameIsActive)
		{
			if (decision && (players[whoseMove].money >= 200))
			{
				stations[players[whoseMove].position].condition = StationCondition.Bought;
				stations[players[whoseMove].position].owner = whoseMove;

				players[whoseMove].money = players[whoseMove].money - 200;
				
				emit stationBought(players[whoseMove].name, players[whoseMove].position);

			    string memory message = string(abi.encodePacked(stations[players[whoseMove].position].name, " is bought"));
				emit actionHappened(players[whoseMove].name, players[whoseMove].position, message);
			}
		
			players[whoseMove].canBuyStation = false;
			whoseMove = ((whoseMove) + 1) % maxNumberOfPlayers;

			return true;
		}

		return false;
	}

	// ------------------------------------------ //
	// ---------|      Events       |------------ //
	// ------------------------------------------ //

	// event for returning dice value
	event moveIsMade(string indexed name, uint8 dice);

	// event for writing log info about current action such as getting into prison and so on
	event actionHappened(string name, uint8 position, string action);

	// event for writing log info about stations purchases
	event stationBought(string indexed name, uint8 station);

	// ------------------------------------------ //
	// ---------| Private functions |------------ //
	// ------------------------------------------ //

	// handle different cases for stations
	function handleStations() private
	{
		// "go to prison" station
		if (players[whoseMove].position == 9)
		{
			emit actionHappened(players[whoseMove].name, players[whoseMove].position, "\nGo to jail station");

			players[whoseMove].position = 3;
			players[whoseMove].movesInPrison = 1; // next move is in prison
		}

		// go station, get 200$
		if (players[whoseMove].position == 0) // "go" station
		{
			players[whoseMove].money += 200;
			emit actionHappened(players[whoseMove].name, players[whoseMove].position, "\nGO station, get 200$");
		}

		// luxury tax station, pay 100$
		if (players[whoseMove].position == 4) // "luxury tax" station
		{
			players[whoseMove].money -= 100;
			emit actionHappened(players[whoseMove].name, players[whoseMove].position, "\nLuxury tax station, pay 100$");
		}

		// chanse station, either get 100$ or pay 100$ or do nothing
		if (players[whoseMove].position == 10) // "chanse" station
		{
			// generate random number for action in this case
			uint256 r = timestampHash();
			uint8 action = uint8((r / 6) % 3); // division by 6 for removing correlation with dice value

			if (action == 0)
			{
				players[whoseMove].money -= 100;
				emit actionHappened(players[whoseMove].name, players[whoseMove].position, "\nChance station, that time pay 100$");
			}
			else if (action == 1)
			{
				players[whoseMove].money += 100;
				emit actionHappened(players[whoseMove].name, players[whoseMove].position, "\nChance station, that time get 100$");
			}
			else
			{
				emit actionHappened(players[whoseMove].name, players[whoseMove].position, "\nChance station, that time do nothing");
			}
		}
	
		// not our station, pay 50$ to owner
		if ((stations[players[whoseMove].position].condition == StationCondition.Bought) && (stations[players[whoseMove].position].owner != whoseMove))
		{
			players[whoseMove].money -= 50;
			players[stations[players[whoseMove].position].owner].money += 50;

			string memory message = string(abi.encodePacked("\nToll station, pay 50$ to ", players[stations[players[whoseMove].position].owner].name));
			emit actionHappened(players[whoseMove].name, players[whoseMove].position, message);
		}

        if (players[whoseMove].money < 0)
        {
            gameIsActive = false;
            emit actionHappened(players[whoseMove].name, players[whoseMove].position, "\nFinished his way");
        }
	}

	// check has this address already signed up for the game
	function isPlayer(address player) private view returns (bool)
	{
		for (uint i=0; i<maxNumberOfPlayers; i++)
		{
			if (players[i].addr == player)
			{
				return true;
			}
		}

		return false;
	}

	// get hash of timestamp of last block - can be considered as random()
	function timestampHash() private view returns (uint256)
	{
		bytes memory timestamp = toBytes(block.timestamp);
		return uint256(keccak256(timestamp));
	}

	// convert to bytes
	function toBytes(uint256 x) private pure returns (bytes memory b)
	{
		b = new bytes(32);
		assembly { mstore(add(b, 32), x) }
	}
}
