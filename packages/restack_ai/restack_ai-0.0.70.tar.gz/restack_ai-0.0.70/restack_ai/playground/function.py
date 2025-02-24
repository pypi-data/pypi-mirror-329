from temporalio import activity


@activity.defn
async def test_run(content: str) -> str:
    return content
