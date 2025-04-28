"""
Loyalty Program API - A simple Python application for managing airline loyalty points
"""

class LoyaltyProgram:
    def __init__(self):
        # In-memory storage for member points
        # { "passenger_name": { "points": 100, "tier": "Silver" } }
        self.members = {}
        self.tier_thresholds = {
            "Bronze": 0,
            "Silver": 5000,
            "Gold": 15000,
            "Platinum": 30000
        }

    def _update_tier(self, passenger_name):
        """Internal method to update member tier based on points."""
        if passenger_name not in self.members:
            return

        points = self.members[passenger_name]["points"]
        current_tier = "Bronze" # Default tier
        for tier, threshold in sorted(self.tier_thresholds.items(), key=lambda item: item[1], reverse=True):
            if points >= threshold:
                current_tier = tier
                break
        self.members[passenger_name]["tier"] = current_tier

    def add_member(self, passenger_name):
        """
        Adds a new member to the loyalty program.

        Args:
            passenger_name (str): The name of the passenger to add.

        Returns:
            bool: True if the member was added successfully, False if they already exist.
        """
        if passenger_name in self.members:
            return False # Member already exists
        self.members[passenger_name] = {"points": 0, "tier": "Bronze"}
        return True

    def get_member_details(self, passenger_name):
        """
        Retrieves the details (points and tier) of a loyalty member.

        Args:
            passenger_name (str): The name of the member.

        Returns:
            dict: Member details if found, otherwise None.
        """
        return self.members.get(passenger_name)

    def add_points(self, passenger_name, points_to_add):
        """
        Adds points to a member's account.

        Args:
            passenger_name (str): The name of the member.
            points_to_add (int): The number of points to add (must be positive).

        Returns:
            bool: True if points were added successfully, False otherwise (e.g., member not found, invalid points).
        """
        if passenger_name not in self.members or points_to_add <= 0:
            return False
        
        self.members[passenger_name]["points"] += points_to_add
        self._update_tier(passenger_name)
        return True

    def redeem_points(self, passenger_name, points_to_redeem):
        """
        Redeems points from a member's account.

        Args:
            passenger_name (str): The name of the member.
            points_to_redeem (int): The number of points to redeem (must be positive).

        Returns:
            bool: True if points were redeemed successfully, False otherwise (e.g., member not found, insufficient points).
        """
        if passenger_name not in self.members or points_to_redeem <= 0:
            return False
        
        member = self.members[passenger_name]
        if member["points"] < points_to_redeem:
            return False # Insufficient points
            
        member["points"] -= points_to_redeem
        self._update_tier(passenger_name) # Tier might change after redemption
        return True

    def get_tier(self, passenger_name):
        """
        Gets the current tier of a member.

        Args:
            passenger_name (str): The name of the member.

        Returns:
            str: The member's tier if found, otherwise None.
        """
        member = self.get_member_details(passenger_name)
        return member["tier"] if member else None

# Example usage
if __name__ == "__main__":
    loyalty = LoyaltyProgram()

    # Add members
    loyalty.add_member("Diana Prince")
    loyalty.add_member("Clark Kent")
    print(f"Added members: {list(loyalty.members.keys())}")

    # Add points
    loyalty.add_points("Diana Prince", 6000)
    loyalty.add_points("Clark Kent", 16000)
    print(f"\nDiana's details: {loyalty.get_member_details('Diana Prince')}")
    print(f"Clark's details: {loyalty.get_member_details('Clark Kent')}")

    # Check tiers
    print(f"\nDiana's tier: {loyalty.get_tier('Diana Prince')}") # Should be Silver
    print(f"Clark's tier: {loyalty.get_tier('Clark Kent')}")   # Should be Gold

    # Redeem points
    redeemed = loyalty.redeem_points("Diana Prince", 2000)
    print(f"\nDiana redeemed 2000 points: {redeemed}")
    print(f"Diana's new details: {loyalty.get_member_details('Diana Prince')}")

    # Try to redeem too many points
    redeemed_fail = loyalty.redeem_points("Clark Kent", 20000)
    print(f"Clark redeemed 20000 points: {redeemed_fail}") # Should be False
    print(f"Clark's details unchanged: {loyalty.get_member_details('Clark Kent')}")
