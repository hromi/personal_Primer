import asyncio

async def handle_gesture(pp):
    while True:
        gesture = await pp.gesture.get_gesture()
        if gesture:
            print(gesture)
            await navigate(pp,gesture)
        await asyncio.sleep(pp.config['gesture']['sleep_time'])

async def navigate(pp,gesture_info):
    if gesture_info:
        try:
            obj_name=gesture_info.get('object')
            obj=getattr(pp,obj_name)
        except:
            print(f"Object {obj_name} not found or method name is missing")
        try:
            method_name=gesture_info.get('method')
            method=getattr(obj,method_name)
        except:
            print(f"Method {method_name} not found in object {obj_name}")
        #print("executing {obj_name}.{method_name}")
        await method()    
   
   #elif gesture == "F" or gesture=="B":
        #await pp.folio.display_current_folio_content()
   #     await pp.queue['display'].put({'b':pp.folio.current_folio['content'].upper()})

