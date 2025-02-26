from aitronos import Aitronos, MessageRequestPayload, Message
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))
import aitronos_logger
from resources import CurrentUser
from resources import Parameters

logger = aitronos_logger.Logger()


def main():
    return "Hello World"


if __name__ == "__main__":
    print(main())