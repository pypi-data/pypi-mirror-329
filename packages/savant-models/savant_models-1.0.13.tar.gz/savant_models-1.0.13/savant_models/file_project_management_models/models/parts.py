from pydantic import ConfigDict, BaseModel, Field


class Parts(BaseModel):

    part_number: int = Field(gt=0, lt=10001)
    etag: str
    model_config = ConfigDict(populate_by_name=True)

    def convert_to_aws(
        self,
    ):
        return {"PartNumber": self.part_number, "ETag": self.etag}

