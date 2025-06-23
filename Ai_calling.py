'''
----------------------------------TO get agent id through python code ------------------------
import os
from omnidimension import Client

api_key = os.environ.get('OMNIDIM_API_KEY', 'Mk1-z2aW4Nq21NEEIanonA45Kis5ZLvyhl5-7YFBWrw')
client = Client(api_key)

# Try to get all agents
try:
    # Method 1: Try different possible API calls
    agents = client.agent.list()
    print("Agents found:")
    for agent in agents:
        print(f"Agent ID: {agent.get('id', agent.get('agent_id'))}")
        print(f"Name: {agent.get('name', 'Unnamed')}")
        print("---")
        
except AttributeError:
    # Method 2: Try alternative API structure
    try:
        agents = client.agents.all()
        print("Agents:", agents)
    except:
        # Method 3: Try direct API call
        try:
            response = client.get('/agents')  # or client.api.get('/agents')
            print("API Response:", response)
        except Exception as e:
            print(f"Error fetching agents: {e}")

'''            
from omnidimension import Client
import json

# ==========================================
# CONFIGURATION - CHANGE THESE VALUES ONLY
# ==========================================
API_KEY = 'Mk1-z2aW4Nq21NEEIanonA45Kis5ZLvyhl5-7YFBWrw'
AGENT_ID = 1791  # Marketing Maven
TARGET_PHONE_NUMBER = "9821238977"  # Put your phone number here (without country code)
COUNTRY_CODE = "+91"  # Change if you're in a different country

# ==========================================

def generate_phone_variations(phone_number, country_code="+91"):
    """
    Generate all possible phone number formats
    """
    # Remove any existing + or country code
    clean_number = phone_number.replace("+", "").replace(" ", "").replace("-", "")
    if clean_number.startswith("91"):
        clean_number = clean_number[2:]  # Remove 91 if present
    
    # Generate all variations
    variations = [
        f"{country_code}{clean_number}",           # +919821238977
        f"{country_code.replace('+', '')}{clean_number}",  # 919821238977
        clean_number,                              # 9821238977
        f"{country_code} {clean_number}",          # +91 9821238977
        f"{country_code} {clean_number[:5]} {clean_number[5:]}", # +91 98212 38977
    ]
    
    return variations

def omnidimension_call_handler():
    """
    Fixed Omnidimension call handler with configurable phone number
    """
    # Initialize client
    client = Client(API_KEY)
    
    # Generate phone number variations
    phone_variations = generate_phone_variations(TARGET_PHONE_NUMBER, COUNTRY_CODE)
    
    print("🚀 Starting Omnidimension Call Process...")
    print("=" * 50)
    print(f"📱 Target Phone: {TARGET_PHONE_NUMBER}")
    print(f"🌍 Country Code: {COUNTRY_CODE}")
    print(f"🔢 Phone Variations: {phone_variations}")
    print("=" * 50)
    
    # Step 1: Verify agent exists and get details
    try:
        print("📋 Step 1: Verifying agent...")
        response = client.get('/agents')
        agents = response['json']['bots']
        
        # Find our agent
        target_agent = None
        for agent in agents:
            if agent['id'] == AGENT_ID:
                target_agent = agent
                break
        
        if not target_agent:
            print(f"❌ Agent {AGENT_ID} not found!")
            return None
            
        print(f"✅ Agent verified:")
        print(f"   Name: {target_agent['name']}")
        print(f"   Type: {target_agent['bot_type']}")
        print(f"   Status: {target_agent['status_of_building_flow']}")
        
    except Exception as e:
        print(f"❌ Error verifying agent: {e}")
        return None
    
    print("\n" + "=" * 50)
    
    # Step 2: Try different call dispatch approaches
    print("📞 Step 2: Dispatching call...")
    print(f"   Agent: {target_agent['name']} (ID: {AGENT_ID})")
    
    # Method 1: Try with data parameter instead of json
    try:
        print(f"\n🔄 Method 1: Using POST with data parameter...")
        for phone in phone_variations:
            try:
                print(f"   Trying: {phone}")
                call_data = {
                    "agent_id": AGENT_ID,
                    "to_number": phone
                }
                response = client.post('/calls/dispatch', data=call_data)
                print(f"✅ SUCCESS! Call dispatched to {phone}!")
                print(json.dumps(response, indent=2))
                return response
            except Exception as phone_error:
                print(f"   ❌ Failed with {phone}: {phone_error}")
                continue
        
    except Exception as e:
        print(f"❌ Method 1 failed: {e}")
    
    # Method 2: Try with bot_id parameter
    try:
        print(f"\n🔄 Method 2: Using bot_id parameter...")
        for phone in phone_variations:
            try:
                print(f"   Trying: {phone}")
                call_data = {
                    "bot_id": AGENT_ID,
                    "to_number": phone
                }
                response = client.post('/calls/dispatch', data=call_data)
                print(f"✅ SUCCESS! Call dispatched to {phone} with bot_id!")
                print(json.dumps(response, indent=2))
                return response
            except Exception as phone_error:
                print(f"   ❌ Failed with {phone}: {phone_error}")
                continue
        
    except Exception as e:
        print(f"❌ Method 2 failed: {e}")
    
    # Method 3: Try client.call.dispatch_call with all variations
    try:
        print(f"\n🔄 Method 3: Using client.call.dispatch_call...")
        for phone in phone_variations:
            try:
                print(f"   Trying: {phone}")
                response = client.call.dispatch_call(AGENT_ID, phone)
                print(f"✅ SUCCESS! Call dispatched to {phone}!")
                print(json.dumps(response, indent=2))
                return response
            except Exception as phone_error:
                print(f"   ❌ Failed with {phone}: {phone_error}")
                continue
                
    except Exception as e:
        print(f"❌ Method 3 failed: {e}")
    
    # Method 4: Try different endpoints
    endpoints = ['/calls/create', '/calls', '/call/dispatch', '/calls/outbound']
    
    for endpoint in endpoints:
        try:
            print(f"\n🔄 Method 4: Using {endpoint} endpoint...")
            for phone in phone_variations:
                try:
                    print(f"   Trying: {phone}")
                    call_data = {
                        "agent_id": AGENT_ID,
                        "to_number": phone,
                        "phone_number": phone,  # Some APIs use different field names
                        "bot_id": AGENT_ID
                    }
                    response = client.post(endpoint, data=call_data)
                    print(f"✅ SUCCESS! Call dispatched to {phone} via {endpoint}!")
                    print(json.dumps(response, indent=2))
                    return response
                except Exception as phone_error:
                    print(f"   ❌ Failed with {phone}: {phone_error}")
                    continue
                    
        except Exception as e:
            print(f"❌ {endpoint} failed: {e}")
    
    print("\n❌ All methods failed!")
    return None

def quick_call():
    """
    Quick call function using the configured phone number
    """
    client = Client(API_KEY)
    phone_variations = generate_phone_variations(TARGET_PHONE_NUMBER, COUNTRY_CODE)
    
    print(f"📞 Quick call: Agent {AGENT_ID}")
    print(f"📱 Phone variations: {phone_variations}")
    
    for phone in phone_variations:
        try:
            print(f"Trying: {phone}")
            response = client.call.dispatch_call(AGENT_ID, phone)
            print(f"✅ SUCCESS with {phone}!")
            print(response)
            return response
        except Exception as e:
            print(f"❌ Failed with {phone}: {e}")
            continue
    
    print("❌ All phone variations failed")
    return None

def update_phone_number(new_phone_number, new_country_code="+91"):
    """
    Helper function to update phone number configuration
    """
    global TARGET_PHONE_NUMBER, COUNTRY_CODE
    TARGET_PHONE_NUMBER = new_phone_number
    COUNTRY_CODE = new_country_code
    
    print(f"📱 Phone number updated to: {new_country_code}{new_phone_number}")
    print(f"🔢 New variations: {generate_phone_variations(new_phone_number, new_country_code)}")

# Main execution
if __name__ == "__main__":
    print("🌟 OMNIDIMENSION CALL SYSTEM - CONFIGURABLE VERSION")
    print("=" * 60)
    print(f"📋 Current Configuration:")
    print(f"   API Key: {API_KEY[:20]}...")
    print(f"   Agent ID: {AGENT_ID}")
    print(f"   Phone: {COUNTRY_CODE}{TARGET_PHONE_NUMBER}")
    print("=" * 60)
    
    # To change phone number, uncomment and modify this line:
    # update_phone_number("9876543210", "+91")  # Replace with your new number
    
    # Run the handler
    result = omnidimension_call_handler()
    
    # If failed, try quick call
    if not result:
        print("\n" + "=" * 40)
        print("🧪 Trying quick call method...")
        quick_call()
    
    print("\n" + "=" * 60)
    print("🏁 Process completed!")
    
    # Show how to change phone number for future use
    print("\n💡 To change phone number in future:")
    print("   Just modify TARGET_PHONE_NUMBER at the top of the file")
    print(f"   Current: TARGET_PHONE_NUMBER = \"{TARGET_PHONE_NUMBER}\"")
    print("   Example: TARGET_PHONE_NUMBER = \"9876543210\"")