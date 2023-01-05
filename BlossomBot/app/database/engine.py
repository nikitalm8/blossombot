from typing import Union, Any, Optional
from .models import Base

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker        


class DatabaseObject(object):


    def __init__(
        self,
        database_url: str,
    ):

        self.engine = create_async_engine(
            database_url, future=True
        )
        self.sessionmaker = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )


    async def create_tables(self, debug: bool=False):

        async with self.engine.begin() as conn:

            if debug:

                await conn.run_sync(Base.metadata.drop_all)
                
            await conn.run_sync(Base.metadata.create_all)


    async def update(
        self, 
        table: str, 
        column: str, 
        value: Any, 
        where: Optional[str]=None,
    ) -> None:

        request = (
            f'UPDATE {table}'
            + f' SET {column} = {value}'
            + (f' WHERE {where}' if where is not None else "")
        )

        async with self.sessionmaker() as session:  # type: ignore

            await session.execute(request)
            await session.commit()


    async def insert(self, instance):

        async with self.sessionmaker() as session:  # type: ignore

            session.add(instance)
            await session.commit()

        return instance


    async def get(
        self, 
        table: str, 
        values: str='*', 
        where: Optional[str]=None,
        join: Optional[str]=None,
        group_by: Optional[str]=None,
        order_by: Optional[str]=None, 
        limit: int=1,
    ) -> Union[list, Any]:
    
        request = (
            f'SELECT {values}'
            + f' FROM {table}'
            + (f' JOIN {join}' if join is not None else "")
            + (f' WHERE {where}' if where is not None else "")
            + (f' GROUP BY {group_by}' if group_by is not None else "")
            + (f' ORDER BY {order_by}' if order_by is not None else "")
            + (f' LIMIT {limit}' if bool(limit) else "")
        )
        async with self.sessionmaker() as session:  # type: ignore

            response = await session.execute(request)
        
        data = [i[0] if len(i) == 1 else list(i) for i in response]

        return data[0] if (limit == 1 and data) else data


    async def delete(self, table: str, where: Union[str, bool]=False) -> None:

        request = (
            f'DELETE FROM {table}'
            + (f' WHERE {where}' if where else "")
        )

        async with self.sessionmaker() as session:  # type: ignore

            await session.execute(request)
            await session.commit()

    
    async def execute(self, *queries: str, commit: bool=True) -> None:

        async with self.sessionmaker() as session:

            for query in queries:
                
                response = await session.execute(query)

            if commit:

                await session.commit()

        return response


async def create_instance(
    database_url: str, 
    debug: bool=False,
) -> DatabaseObject:

    instance = DatabaseObject(
        database_url=database_url,
    )
    await instance.create_tables(debug=debug)

    return instance
