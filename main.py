import argparse
import asyncio
import enum

import dotenv
import uvicorn


class RunType(enum.Enum):
    app = enum.auto()
    scheduler = enum.auto()
    shell = enum.auto()

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_string(cls, string: str) -> "RunType":
        try:
            return RunType[string]
        except KeyError:
            raise ValueError()


if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--type", type=RunType.from_string, choices=list(RunType))
    run_type: RunType = parser.parse_args().type

    match run_type:
        case RunType.app:
            uvicorn.run("app:create_app", factory=True, reload=True)
        case RunType.scheduler:
            import scheduler

            asyncio.run(scheduler.main())
        case RunType.shell:
            pass
