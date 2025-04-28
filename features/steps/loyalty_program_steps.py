from behave import *
from app import LoyaltyProgram

@given("the loyalty program system is initialized")
def step_impl(context):
    context.loyalty = LoyaltyProgram()
    context.operation_status = {}

@when("I add a new member \"{member_name}\"")
def step_impl(context, member_name):
    context.operation_status["add_member"] = context.loyalty.add_member(member_name)
    context.current_member = member_name

@then("the member should be added successfully")
def step_impl(context):
    assert context.operation_status.get("add_member") is True, f"Member {context.current_member} was not added successfully"
    member_details = context.loyalty.get_member_details(context.current_member)
    assert member_details is not None, f"Member {context.current_member} not found after adding"

@then("the member should have {points:d} points")
def step_impl(context, points):
    member_details = context.loyalty.get_member_details(context.current_member)
    assert member_details["points"] == points, f"Expected {points} points for {context.current_member}, but got {member_details["points"]}"

@then("the member should be in the \"{tier}\" tier")
def step_impl(context, tier):
    member_details = context.loyalty.get_member_details(context.current_member)
    assert member_details["tier"] == tier, f"Expected tier {tier} for {context.current_member}, but got {member_details["tier"]}"

@given("there is a member \"{member_name}\"")
def step_impl(context, member_name):
    # Ensure member exists, add if not
    if not context.loyalty.get_member_details(member_name):
        context.loyalty.add_member(member_name)
    context.current_member = member_name

@given("there is a member \"{member_name}\" with {points:d} points")
def step_impl(context, member_name, points):
    # Ensure member exists and set points
    if not context.loyalty.get_member_details(member_name):
        context.loyalty.add_member(member_name)
    # Directly set points for the test setup (bypassing add_points logic for setup)
    context.loyalty.members[member_name]["points"] = points
    context.loyalty._update_tier(member_name) # Update tier after setting points
    context.current_member = member_name

@when("I add {points:d} points to \"{member_name}\"")
def step_impl(context, points, member_name):
    context.operation_status["add_points"] = context.loyalty.add_points(member_name, points)
    context.current_member = member_name

@then("the points should be added successfully")
def step_impl(context):
    assert context.operation_status.get("add_points") is True, f"Points were not added successfully for {context.current_member}"

@then("\"{member_name}\" should have {points:d} points")
def step_impl(context, member_name, points):
    member_details = context.loyalty.get_member_details(member_name)
    assert member_details["points"] == points, f"Expected {points} points for {member_name}, but got {member_details["points"]}"

@then("\"{member_name}\" should be in the \"{tier}\" tier")
def step_impl(context, member_name, tier):
    member_details = context.loyalty.get_member_details(member_name)
    assert member_details["tier"] == tier, f"Expected tier {tier} for {member_name}, but got {member_details["tier"]}"

@when("I redeem {points:d} points from \"{member_name}\"")
def step_impl(context, points, member_name):
    context.operation_status["redeem_points"] = context.loyalty.redeem_points(member_name, points)
    context.current_member = member_name

@when("I attempt to redeem {points:d} points from \"{member_name}\"")
def step_impl(context, points, member_name):
    # Same as redeem, but used for negative scenarios
    context.operation_status["redeem_points"] = context.loyalty.redeem_points(member_name, points)
    context.current_member = member_name

@then("the points should be redeemed successfully")
def step_impl(context):
    assert context.operation_status.get("redeem_points") is True, f"Points were not redeemed successfully for {context.current_member}"

@then("the redemption should fail")
def step_impl(context):
    assert context.operation_status.get("redeem_points") is False, f"Points were redeemed successfully for {context.current_member} when it should have failed"

@then("\"{member_name}\" should still have {points:d} points")
def step_impl(context, member_name, points):
    # Verify points haven't changed after failed redemption
    member_details = context.loyalty.get_member_details(member_name)
    assert member_details["points"] == points, f"Expected {points} points for {member_name} after failed redemption, but got {member_details["points"]}"

@then("the member should not be added")
def step_impl(context):
    assert context.operation_status.get("add_member") is False, f"Member {context.current_member} was added successfully when they should already exist"

@then("the points should not be added")
def step_impl(context):
    assert context.operation_status.get("add_points") is False, f"Invalid points were added successfully for {context.current_member}"
