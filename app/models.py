from elixir import metadata, Entity, Field
from elixir import Unicode, UnicodeText, JsonType

class Finra(Entity):
	using_option(tablename='finradb')
	Info = Field(JsonType()) 
	OthrNms = Field(JsonType())
	CrntEmps = Field(JsonType())
	Exms = Field(JsonType())
	Dsgntns = Field(JsonType())
	PrevRgstns = Field(JsonType())
	EmpHss = Field(JsonType())
	OthrBuss = Field(JsonType()) 
	DRPs = Field(JsonType())

