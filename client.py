from web3 import HTTPProvider, Web3
import json

class Client:
    def __init__(self, contractAddress, clientName, clientAddress, netAddress='http://127.0.0.1:7545',
                verbose = False):
        
        self.web3 = Web3(HTTPProvider(netAddress))
        
        self.contractAddress = contractAddress
        self.clientName = clientName
        self.clientAddress = clientAddress
        self.verbose = verbose
        
        self.web3.eth.defaultAccount = self.clientAddress

        if self.verbose:
            if self.web3.isConnected():
                print("Test net is connected")
            else:
                print("Problem with connection to test net")
        
        abi = json.load(open('contract/build/contracts/Monopoly.json'))['abi']
        self.contract = self.web3.eth.contract(address=contractAddress, abi=abi)
        
        self.filterMoveIsMade = self.contract.events.moveIsMade.createFilter(fromBlock="latest", 
                                                    argument_filters={'name':self.clientName})
        self.filterStationBought = self.contract.events.stationBought.createFilter(fromBlock="latest",
                                                    argument_filters={'name':self.clientName})
        self.filterActionHappened = self.contract.events.actionHappened.createFilter(fromBlock="latest")

    
    def enrollGame(self, verbose=False):
        enrollSuccess = self.contract.functions.enroll(self.clientName).call()
        
        tx_hash = self.contract.functions.enroll(self.clientName).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        
        [getNumberSuccess, self.playerNumber] = self.contract.functions.getNumberOfYourPlayer().call()

        if verbose or self.verbose:
            print(self.clientName, "Enroll success:", enrollSuccess)
            print(self.clientName, "Enroll transact status:",tx_receipt.status)
            
            if getNumberSuccess:
                print(self.clientName, "Your player number", self.playerNumber)
            else:
                print(self.clientName, "Error while getting number of player")
        
        return getNumberSuccess and enrollSuccess
    
    def isGameActive(self, verbose=False):
        isActive = self.contract.functions.isGameActive().call()
        if verbose or self.verbose:
            print("game is active:", isActive)

        return isActive
    
    def isDecisionNecessary(self, verbose=False):
        isNecessary = self.contract.functions.getPlayerByIndex(self.playerNumber).call()[5]
        
        if verbose or self.verbose:
            if isNecessary:
                print(self.clientName, "decision IS necessary")
            else:
                print(self.clientName, "decision is NOT necessary")
                
        return isNecessary

    def whoseMove(self, verbose=False):
        whose = self.contract.functions.getWhoseMove().call()
        
        if verbose or self.verbose:
            print("whose move:", whose)
            
        return whose
    
    def movesInPrison(self, verbose=False):
        movesInPr = self.contract.functions.getPlayerByIndex(self.playerNumber).call()[4]

        if verbose or self.verbose:
            if movesInPr > 0:
                print(self.clientName, "has", movesInPr, "moves in prison")
            else:
                print(self.clientName, "is NOT in prison")

        return movesInPr
    
    def makeMove(self, verbose=False):
        if self.contract.functions.getWhoseMove().call() != self.clientName:
            if verbose or self.verbose:
                print(self.clientName, "It's not your move")
            dice = -1
            return dice
        
        makeMoveSuccess = self.contract.functions.makeMove().call()

        tx_hash=self.contract.functions.makeMove().transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)        
        events=self.filterMoveIsMade.get_new_entries()

        if (tx_receipt.status != 1) or (len(events) == 0):
            dice = -1
        else:
            dice = events[len(events)-1]['args']['dice']

        if verbose or self.verbose:
            print(self.clientName, "MakeMove success:", makeMoveSuccess)
            print(self.clientName, "makeMove transact status",tx_receipt.status)
            if len(events) > 0:
                print(self.clientName, "Dice value:", dice)
                if len(events) > 1:
                    print(self.clientName, "Bug, there are more events MoveIsMade")
            else:
                print(self.clientName, "no events with moves")
                
        return dice

    def getPlayers(self):
        players = {}
        maxNumber = self.contract.functions.getMaxNumberOfPlayers().call()
        for i in range(maxNumber):
            player = self.contract.functions.getPlayerByIndex(i).call()
            players[player[1]]={"money":player[2], "position":player[3], "moves in prison":player[4]}
        return players     
    
    def getPositions(self):
        positions = []
        numberOfPositions = self.contract.functions.getNumberOfStations().call()
        players = self.getPlayers()

        for i in range(numberOfPositions):
            [state, owner] = self.contract.functions.getStationByIndex(i).call()
            if state == 0:
                positions.append(["None",""])
            if state == 1:
                positions.append(["Available", ""])
            if state == 2:
                positions.append(["Bought", self.contract.functions.getPlayerByIndex(owner).call()[1]])

        return positions
    
    def getLogs(self, verbose=True):
        logs = []
        events = self.filterActionHappened.get_new_entries()
        
        for event in events:
            logs.append(str(event['args']['name']) + " at position " + 
                        str(event['args']['position']) + " : " + str(event['args']['action']))
        
        if verbose or self.verbose:
                for log in logs:
                    print(log)
        
        return logs

    def makeDecision(self, decision, verbose=False):
        makeDecisionSuccess = self.contract.functions.buyStation(decision).call()
        
        tx_hash=self.contract.functions.buyStation(decision).transact()
        tx_receipt = self.web3.eth.waitForTransactionReceipt(tx_hash)
        events=self.filterStationBought.get_new_entries()
        
        if verbose or self.verbose:
            print(self.clientName, "makeDecision success:", makeDecisionSuccess)
            print(self.clientName, "makeDecision transact status:",tx_receipt.status)

            if len(events) > 0:
                print("station",events[len(events)-1]['args']['station'], "is bought by you")
                print("current money:", self.contract.functions.getPlayerByIndex(self.playerNumber).call()[2])
                
                if len(events) > 1:
                    print("there are also more events")
            else:
                print("station is not bought by you")
                print("current money:", self.contract.functions.getPlayerByIndex(self.playerNumber).call()[2])
        
        return makeDecisionSuccess and (len(events) > 0)
