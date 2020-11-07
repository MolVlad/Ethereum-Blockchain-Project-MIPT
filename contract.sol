// contract.sol
pragma solidity ^0.4.21;
contract simplestorage {
  uint public storedData;
  event Updated(address by, uint _old, uint _new);
  function set(uint x) {
    uint old = storedData;
    storedData = x;
    emit Updated(msg.sender, old, x);
  }
  function get() constant returns (uint retVal) {
    return storedData;
  }
}
