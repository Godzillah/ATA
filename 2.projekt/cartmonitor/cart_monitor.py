#!/usr/bin/env python3
"""
Dynamic analyser of a cart controller.
"""


class LoadCountDestination:
    def __init__(self):
        self.load_count = 0
        self.destination = "A"


class Feature:
    def __init__(self):
        self.full_slots = 0
        self.capacity = 0
        self.requests = []
        self.load_count_destination = LoadCountDestination()
        self.cart_slots_status = {
            "0": "empty",
            "1": "empty",
            "2": "empty",
            "3": "empty",
            "4": "empty",
            "5": "empty"
        }
        # statistic instance variables
        self.tracks_count = 0
        self.full_slots_summary = 0
        self.property_failures = []


feature = Feature()


def report_coverage():
    "Coverage reporter"
    # All def-coverage
    # f.e 4 tracks, 4 slots = every path were 1/4 -> 25%
    #                         every path were 2/4 -> 50%
    #                         every path were 4/4 -> 100%
    print('CartCoverage %d%%' % ((feature.full_slots_summary / (feature.tracks_count * 4)) * 100))


def on_moving(time, pos1, pos2):
    "priklad event-handleru pro udalost moving"
    # vsechny parametry jsou typu str; nektere muze byt nutne pretypovat

    feature.full_slots_summary += feature.full_slots
    feature.tracks_count += 1
    # print('%s:debug: got moving from %s to %s' % (time, pos1, pos2))


def on_requesting(time, position_from, position_to, gear, weight_of_gear):
    # print('%s:debug: requesting gear %s with weight %s with road from position %s to position %s ' % (
    #     time, gear, weight_of_gear, position_from, position_to))

    feature.requests.append(position_from + "," + gear + "," + weight_of_gear + "," + position_to)


def on_loading(time, position, gear, weight_of_gear, loading_slot):
    # print('%s:debug: loading gear %s with weight %s to slot %s in %s position' % (
    #     time, gear, weight_of_gear, loading_slot, position))

    # MONITOR_1: Vozík nesmí nakládat na obsazený slot.
    if feature.cart_slots_status[loading_slot] == "full":
        # print(time + ":error loading into an occupied slot with number " + loading_slot)
        feature.property_failures.append(time + ":error loading into an occupied slot with number " + loading_slot)

    feature.cart_slots_status[loading_slot] = "full"

    # MONITOR 5: Vozík nesmí nakládat ve stanici, pokud na to ne-existovala žádost.

    if len(feature.requests) == 0:
        # print(time + ":error loading '%s' that has not been requested by controller " % gear)
        feature.property_failures.append(time + ":error loading '%s' that has not been requested by controller " % gear)
    else:
        has_found = False
        for request in feature.requests:
            request = request.split(",")
            if request[0] == position and request[1] == gear and request[2] == weight_of_gear:
                # print("%s:debug:request for '%s' with weight '%s' exist from position '%s'" % (time, gear, weight_of_gear, position))
                has_found = True
        if not has_found:
            # print(time + ":error loading '%s' in position %s with weight %s that has not been requested by controller "
            #       % (gear, position, weight_of_gear))
            feature.property_failures.append(time + ":error loading '%s' in position %s with weight %s that has not been "
                                                    "requested by controller " % (gear, position, weight_of_gear))

    # MONITOR 6: Nesmí být naloženo více než 4 náklady
    if feature.full_slots > 4:
        # print(time + ":error overflow cart slots current " + str(feature.full_slots) + " but only 4 are allowed!")
        feature.property_failures.append(
            time + ":error overflow cart slots current " + str(feature.full_slots) + " but only 4 are allowed!")
        # MONITOR 7: Vozík nesmí být přetížen
    if feature.capacity > 150:
        # print(time + ":error overflow cart capacity current " + str(feature.capacity) + " but only 150 are allowed!")
        feature.property_failures.append(
            time + ":error overflow cart capacity current " + str(feature.capacity) + " but only 150 are allowed!")

    feature.load_count_destination.load_count = + 1
    feature.load_count_destination.destination = position
    feature.full_slots += 1
    feature.capacity += int(weight_of_gear)
    # print('debug:Current full slots %s/4, current capacity of cart %s/150' % (current_slots, current_capacity))

def on_unloading(time, position, gear, weight_of_gear, unloading_slot):
    # print('%s:debug: unloading gear %s with weight %s to slot %s in %s position' % (
    #     time, gear, weight_of_gear, unloading_slot, position))

    # MONITOR_2: Vozík nesmí vykládat z volného slotu
    if feature.cart_slots_status[unloading_slot] == "empty":
        # print(time + ":error unloading empty slot with number " + unloading_slot)
        feature.property_failures.append(time + ":error unloading empty slot with number " + unloading_slot)

    # MONITOR_3: Náklad se musí vyložit, pokud je vozík v cílové stanici daného nákladu
    if position == feature.load_count_destination.destination and feature.load_count_destination.load_count > 0:
        # print("%s:debug:unloading for '%s' with weight '%s' successfully unloaded in the destination position %s" % (
        #     time, gear, weight_of_gear, position))
        feature.load_count_destination.load_count -= 1

        # print(time + ":error gear '%s' with weight %s was not unloaded in the destination position %s"
        #       % (gear, weight_of_gear, position))

    feature.cart_slots_status[unloading_slot] = "empty"
    feature.full_slots -= 1
    feature.capacity -= int(weight_of_gear)

def on_event(event):
    # print(event)

    event_id = event[1]
    del (event[1])

    # MONITOR_1: Vozík nesmí nakládat na obsazený slot.
    # MONITOR 5: Vozík nesmí nakládat ve stanici, pokud na to neexistovala žádost.
    # MONITOR 6: Nesmí být naloženo více než 4 náklady
    # MONITOR 7: Vozík nesmí být přetížen
    if event_id == 'loading':
        on_loading(*event)
    # MONITOR_2: Vozík nesmí vykládat z volného slotu
    # MONITOR_3: Náklad se musí vyložit, pokud je vozík v cílové stanici daného nákladu
    elif event_id == 'unloading':
        on_unloading(*event)
    elif event_id == 'requesting':
        on_requesting(*event)
    elif event_id == 'moving':
        on_moving(*event)


###########################################################
# Nize netreba menit.

def monitor(reader):
    "Main function"
    for line in reader:
        line = line.strip()
        on_event(line.split())

    if len(feature.property_failures) == 0:
        print("All properties hold.")
    else:
        print(*feature.property_failures, sep='\n')
    report_coverage()


if __name__ == "__main__":
    import sys

    monitor(sys.stdin)
