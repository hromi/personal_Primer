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
        await pp.folio.descend()

    elif gesture == "U":
        await pp.folio.ascend()

    elif gesture == "R":
        await pp.folio.next_folio()

    elif gesture == "L":
        await pp.folio.previous_folio()

    elif gesture == "A":
        await pp.student.logout()

    elif gesture == "F" or gesture=="B":
        await pp.folio.display_current_folio_content()

