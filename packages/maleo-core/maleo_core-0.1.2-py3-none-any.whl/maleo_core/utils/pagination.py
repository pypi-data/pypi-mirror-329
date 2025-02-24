from maleo_core.models.dto import BaseDTO

def generate(
    page_number:int,
    limit:int,
    data_count:int,
    total_data:int
) -> BaseDTO.Pagination:
    pagination = BaseDTO.Pagination(
        page_number=page_number,
        data_count=data_count,
        total_data=total_data,
        total_pages=(total_data // limit) + (1 if total_data % limit > 0 else 0)
    )
    return pagination