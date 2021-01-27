#!/usr/bin/env python3
import json

from characteritics import SlotCharacteristic, CapacityCharacteristic

"""
Example of usage/test of Cart controller implementation.
"""

from cartctl import CartCtl, reset_scheduler
from cart import Cart, Load, Status, CartError
import jarvisenv

global move_count

def prepare_easy_path():
    helmet = Load('A', 'B', 20, 'helmet')
    helmet.onload = on_load
    helmet.onunload = on_unload

    return helmet


def prepare_medium_path():
    helmet = Load('A', 'B', 20, 'helmet')
    helmet.onload = on_load
    helmet.onunload = on_unload

    heart = Load('C', 'A', 40, 'heart')
    heart.onload = on_load
    heart.onunload = on_unload

    braceletR = Load('D', 'C', 40, 'braceletR')
    braceletR.onload = on_load
    braceletR.onunload = on_unload

    braceletL = Load('D', 'C', 40, 'braceletL')
    braceletL.onload = on_load
    braceletL.onunload = on_unload

    return helmet, heart, braceletR, braceletL


def prepare_hardcore_path():
    helmet = Load('A', 'B', 20, 'helmet')
    helmet.onload = on_load
    helmet.onunload = on_unload

    heart = Load('C', 'A', 40, 'heart')
    heart.onload = on_load
    heart.onunload = on_unload

    braceletR = Load('D', 'C', 40, 'braceletR')
    braceletR.onload = on_load
    braceletR.onunload = on_unload

    braceletL = Load('D', 'C', 40, 'braceletL')
    braceletL.onload = on_load
    braceletL.onunload = on_unload

    legR = Load('C', 'D', 30, 'legR')
    legR.onload = on_load
    legR.onunload = on_unload

    legL = Load('C', 'D', 30, 'legL')
    legL.onload = on_load
    legL.onunload = on_unload

    head = Load('B', 'A', 30, 'head')
    head.onload = on_load
    head.onunload = on_unload

    return helmet, heart, braceletR, braceletL, legR, legL, head


def on_move(c: Cart):
    "example callback (for assert)"
    "We have three types of capacity, which can have a Cart: 50kg, 150kg, 500kg"
    assert c.load_capacity == 50 or c.load_capacity == 150 or c.load_capacity == 500
    "Cart has from 1 to 4 slots"
    assert 1 <= len(c.slots) <= 4

    if c.load_capacity == 50 or c.load_capacity == 150:
        assert 2 <= len(c.slots) <= 4
    else:
        # cart with load_capacity=500kg has 1 or 2 slots
        assert 1 <= len(c.slots) <= 2

    assert c.status == Status.Moving

    global move_count
    move_count += 1

    print('%d: Cart is moving %s->%s' % (jarvisenv.time(), c.pos, c.data))


def on_load(c: Cart, load: Load):
    assert c.status == Status.Loading or c.status == Status.Idle
    print('%d: Cart at %s: loading: %s' % (jarvisenv.time(), c.pos, load))


def on_unload(c: Cart, load: Load):
    assert c.status == Status.Loading or c.status == Status.Idle

    print('%d: Cart at %s: unloading: %s' % (jarvisenv.time(), c.pos, load))
    if load.content == 'helmet':
        assert c.pos == 'B'
    if load.content == 'heart' or load.content == 'head':
        assert c.pos == 'A'
    if load.content.startswith('bracelet'):
        assert c.pos == 'C'
    if load.content.startswith('leg'):
        assert c.pos == 'D'


def add_load(c: CartCtl, load: Load):
    "callback for schedulled load"
    c.request(load)


def setUpCart(slot_count, capacity):
    cart_dev = Cart(slot_count, capacity)
    cart_dev.onmove = on_move

    return cart_dev


def test_suite():
    with open("generatedData/dataT3.json") as json_file:
        global move_count
        move_count = 0
        test_suite = json.load(json_file)
        test_count = 0
        test_success_count = 0
        test_fail_count = 0
        failed_tests = []

        for test_case in test_suite:
            test_count += 1
            print("========= STARTING TEST CASE " + str(test_count) + " ===========\n")

            try:
                cart_dev = setUpCart(test_case[0], test_case[1])
                cart_controller = CartCtl(cart_dev, jarvisenv.JARVIS_TRACKS)

                if test_case[2] == "easy":
                    item = prepare_easy_path()

                    s = reset_scheduler()

                    s.enter(10, 0, add_load, (cart_controller, item))

                elif test_case[2] == "medium":
                    item = prepare_medium_path()

                    s = reset_scheduler()

                    if test_case[3]:
                        s.enter(10, 0, add_load, (cart_controller, item[0]))
                        s.enter(10, 0, add_load, (cart_controller, item[1]))
                        s.enter(10, 0, add_load, (cart_controller, item[2]))
                        s.enter(10, 0, add_load, (cart_controller, item[3]))
                    else:
                        s.enter(10, 0, add_load, (cart_controller, item[0]))
                        s.enter(45, 0, add_load, (cart_controller, item[1]))
                        s.enter(25, 0, add_load, (cart_controller, item[2]))
                        s.enter(30, 0, add_load, (cart_controller, item[3]))


                elif test_case[2] == "hardcore":
                    item = prepare_hardcore_path()

                    s = reset_scheduler()

                    if test_case[3]:
                        s.enter(10, 0, add_load, (cart_controller, item[0]))
                        s.enter(45, 0, add_load, (cart_controller, item[1]))
                        s.enter(25, 0, add_load, (cart_controller, item[2]))
                        s.enter(30, 0, add_load, (cart_controller, item[3]))
                        s.enter(80, 0, add_load, (cart_controller, item[4]))
                        s.enter(120, 0, add_load, (cart_controller, item[5]))
                        s.enter(140, 0, add_load, (cart_controller, item[6]))
                    else:
                        s.enter(2, 0, add_load, (cart_controller, item[0]))
                        s.enter(2, 0, add_load, (cart_controller, item[1]))
                        s.enter(2, 0, add_load, (cart_controller, item[2]))
                        s.enter(2, 0, add_load, (cart_controller, item[3]))
                        s.enter(2, 0, add_load, (cart_controller, item[4]))
                        s.enter(2, 0, add_load, (cart_controller, item[5]))
                        s.enter(2, 0, add_load, (cart_controller, item[6]))

                # Exercise & Verify
                s.run()

                print(cart_dev)
                print("Test case - " + str(test_count) + " was successful")

                test_success_count += 1
                print("========= ENDING TEST CASE " + str(test_count) + " ===========\n")
            except CartError as ce:
                if ce.__eq__("Cart is busy: Status.Loading"):
                    print("Excepted error because we invoke all requests in the same time - Cart is busy: "
                          "Status.Loading")
                    print("========= ENDING TEST CASE " + str(test_count) + " ===========\n")
                    test_success_count += 1
                    continue
                else:
                    error_message = "CartError:Test case " + str(
                        test_count) + " with following configuration failed " + str(test_case) + " with message " + str(
                        ce)
                    print(error_message)
                    failed_tests.append(error_message)
                    test_fail_count += 1
                    print("========= ENDING TEST CASE " + str(test_count) + " ===========\n")
            except AssertionError as ae:
                error_message = "AssertionError:Test case " + str(
                    test_count) + " with following configuration failed " + str(test_case) + " with message " + str(ae)
                print(error_message)
                failed_tests.append(error_message)
                test_fail_count += 1
                print("========= ENDING TEST CASE " + str(test_count) + " ===========\n")

        print("==========================================================")

        print("List of failed tests:")
        print(*failed_tests, sep='\n')

        print("==========  SUMMARY OF CHAINING TESTS ==========")
        print("Tests success " + str(test_success_count))
        print("Tests failed " + str(test_fail_count))
        print("==========================================================")
        print("\n")


def test_case_cart_not_pick_the_item_because_of_huge_weight():
    cart_dev = setUpCart(SlotCharacteristic.THREE_SLOTS.value, CapacityCharacteristic.LIGHT_CAPACITY.value)
    cart_controller = CartCtl(cart_dev, jarvisenv.JARVIS_TRACKS)

    global move_count
    move_count = 0

    helmet = Load('A', 'B', 1000, 'helmet')
    helmet.onload = on_load
    helmet.onunload = on_unload

    s = reset_scheduler()

    s.enter(10, 0, add_load, (cart_controller, helmet))

    # Exercise & Verify
    s.run()

    print("Excepting that Cart does not move and move_count is 0 because of 1000kg weight that is not acceptable")
    assert move_count == 0;

def test_case_cart_move_only_once():
    cart_dev = setUpCart(SlotCharacteristic.TWO_SLOTS.value, CapacityCharacteristic.HEAVY_CAPACITY.value)
    cart_controller = CartCtl(cart_dev, jarvisenv.JARVIS_TRACKS)

    global move_count
    move_count = 0

    item = prepare_easy_path()

    s = reset_scheduler()

    s.enter(10, 0, add_load, (cart_controller, item))

    # Exercise & Verify
    s.run()

    print("Excepting that Cart move only once of from A -> B")
    assert move_count == 1;

def main():
    "main test suite"
    test_suite()
    test_case_cart_not_pick_the_item_because_of_huge_weight()
    test_case_cart_move_only_once()

if __name__ == "__main__":
    test_suite()
    test_case_cart_not_pick_the_item_because_of_huge_weight()
    test_case_cart_move_only_once()
