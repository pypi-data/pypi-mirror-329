from aitronos import Aitronos, MessageRequestPayload, Message
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
import aitronos_logger
from resources import CurrentUser

logger = aitronos_logger.Logger()


def main():
    try:
        # Start time estimation for the whole process
        logger.info("Starting hello world project execution", component="HelloWorld", progress=0, remaining_time_seconds=5)
        
        # Initialize user
        current_user = CurrentUser()
        user = current_user.user
        logger.info(f"User authenticated: {user.full_name}", component="UserManagement", progress=20, remaining_time_seconds=4)
        
        # Initialize Aitronos
        assistant_messaging = Aitronos(api_key=user.user_token).AssistantMessaging
        logger.info("Aitronos assistant messaging initialized", component="AitronosSetup", progress=40, remaining_time_seconds=3)
        
        # Create and send message
        payload = MessageRequestPayload(
            organization_id=user.current_organization_id,
            assistant_id=1,
            instructions="You are a friendly greeter who loves making people smile with fun welcome messages.",
            messages=[Message(
                content=f"Welcome {user.full_name} to the world with a warm and creative message!",
                role="user"
            )]
        )
        logger.info("Message payload created", component="MessagePreparation", progress=60, remaining_time_seconds=2)
        
        response = assistant_messaging.execute_run(payload=payload)
        logger.info("Welcome message generated", component="MessagePreparation", progress=100, remaining_time_seconds=0)
        
        return response
        
    except Exception as e:
        logger.error(f"Hello world execution failed: {str(e)}", component="HelloWorld", severity=4, exc=e)
        raise


if __name__ == "__main__":
    print(main())