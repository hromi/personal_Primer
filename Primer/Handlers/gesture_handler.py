import asyncio

async def handle_gesture(pp):
    while True:
        gesture = await pp.gesture.get_gesture()
        if gesture:
            print(gesture)
            await navigate(pp,gesture)
        await asyncio.sleep(0.1)

async def navigate(pp,gesture):
    if gesture == "D":
        children = pp.folio.current_folio.get('children', [])
        if children:
            pp.folio.siblings=children
            # Move to the first child of the current folio
            # Push the current folio and index to the path
            pp.folio.path.append((pp.folio.current_folio, 0))
            pp.folio.current_folio = children[0]
            await pp.folio.activate_current_folio()

    elif gesture == "U":
        if pp.folio.path:
            # Pop the last parent folio and index from the path
            print(pp.folio.path[-1][0])
            #pp.folio.siblings=pp.folio.path[-1][0]['children']
            pp.folio.current_folio, _ = pp.folio.path.pop()
            pp.folio.siblings=pp.folio.path[-1][0]['children']
            #pp.folio.siblings=pp.folio.path[-1]['children']
            await pp.folio.activate_current_folio()
    elif gesture == "R":
        if pp.folio.siblings:
            # Move to the next sibling folio
            pp.folio.sibling_index = (pp.folio.sibling_index + 1) % len(pp.folio.siblings)
            pp.folio.current_folio = pp.folio.siblings[pp.folio.sibling_index]
            await pp.folio.activate_current_folio()

    elif gesture == "L":
        if pp.folio.siblings:
            # Move to the previous sibling folio
            pp.folio.sibling_index = (pp.folio.sibling_index - 1) % len(pp.folio.siblings)
            pp.folio.current_folio = pp.folio.siblings[pp.folio.sibling_index]
            await pp.folio.activate_current_folio()
