#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import pytest
from typing import Tuple, List
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress
from bitcoin.signmessage import BitcoinMessage, SignMessage
from hivemind import HivemindState, HivemindIssue, HivemindOption, HivemindOpinion

def generate_bitcoin_keypair() -> Tuple[CBitcoinSecret, str]:
    """Generate a random Bitcoin private key and its corresponding address.
    
    Returns:
        Tuple[CBitcoinSecret, str]: (private_key, address) pair where address is in base58 format
    """
    entropy = random.getrandbits(256).to_bytes(32, byteorder='big')
    private_key = CBitcoinSecret.from_secret_bytes(entropy)
    address = str(P2PKHBitcoinAddress.from_pubkey(private_key.pub))
    return private_key, address

def sign_message(message: str, private_key: CBitcoinSecret) -> str:
    """Sign a message with a Bitcoin private key.
    
    Args:
        message: The message to sign
        private_key: Bitcoin private key
        
    Returns:
        str: The signature in base64 format
    """
    return SignMessage(key=private_key, message=BitcoinMessage(message)).decode()

# Common Fixtures
@pytest.fixture
def state() -> HivemindState:
    """Create a fresh HivemindState instance for each test."""
    return HivemindState()

@pytest.fixture
def basic_issue() -> HivemindIssue:
    """Create a basic issue for testing."""
    issue = HivemindIssue()
    issue.name = "Test Issue"
    issue.add_question("Test Question")
    issue.description = "Test Description"
    issue.tags = ["test"]
    issue.answer_type = "String"
    issue.constraints = {}
    issue.restrictions = {}
    return issue

@pytest.fixture
def color_choice_issue(basic_issue) -> HivemindIssue:
    """Create an issue with color choices."""
    basic_issue.set_constraints({
        "choices": [
            {"value": "red", "text": "Red"},
            {"value": "blue", "text": "Blue"},
            {"value": "green", "text": "Green"}
        ]
    })
    return basic_issue

@pytest.fixture
def bool_issue(basic_issue) -> HivemindIssue:
    """Create a boolean issue."""
    basic_issue.answer_type = "Bool"
    basic_issue.set_constraints({
        "true_value": "Yes",
        "false_value": "No"
    })
    return basic_issue

@pytest.fixture
def test_keypair() -> Tuple[CBitcoinSecret, str]:
    """Generate a consistent test keypair."""
    return generate_bitcoin_keypair()

class TestHelper:
    """Helper class containing common test operations."""
    
    @staticmethod
    def create_and_sign_option(state: HivemindState, issue_hash: str, value: str, text: str, 
                             private_key: CBitcoinSecret, address: str, timestamp: int) -> str:
        """Helper to create and sign an option.
        
        Args:
            state: HivemindState instance
            issue_hash: Hash of the issue
            value: Option value
            text: Option display text
            private_key: Signer's private key
            address: Signer's address
            timestamp: Current timestamp
            
        Returns:
            str: Hash of the created option
        """
        option = HivemindOption()
        option.set_hivemind_issue(issue_hash)
        option.set(value=value)
        option.text = text
        option_hash = option.save()
        
        message = f"{timestamp}{option_hash}"
        signature = sign_message(message, private_key)
        state.add_option(timestamp, option_hash, address, signature)
        return option_hash

    @staticmethod
    def create_and_sign_opinion(state: HivemindState, issue_hash: str, ranking: List[str],
                              private_key: CBitcoinSecret, address: str, timestamp: int) -> str:
        """Helper to create and sign an opinion.
        
        Args:
            state: HivemindState instance
            issue_hash: Hash of the issue
            ranking: List of option hashes in preferred order
            private_key: Signer's private key
            address: Signer's address
            timestamp: Current timestamp
            
        Returns:
            str: Hash of the created opinion
        """
        opinion = HivemindOpinion()
        opinion.hivemind_id = issue_hash
        opinion.question_index = 0
        opinion.ranking.set_fixed(ranking)  # First address prefers red > blue > green
        opinion.ranking = opinion.ranking.get()  # Get serializable representation
        opinion_hash = opinion.save()  # Save will use the data we just set
        
        message = f"{timestamp}{opinion_hash}"
        signature = sign_message(message, private_key)
        state.add_opinion(timestamp, opinion_hash, signature, address)
        return opinion_hash
