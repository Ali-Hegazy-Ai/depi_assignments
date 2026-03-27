# Assignment 01 – End-to-End ETL Workflow

**Topic:** Fetching data from a public API, cleaning it, and persisting results

| Field | Value |
|---|---|
| Student Name | *(your name)* |
| Date | *(today's date)* |

## Objective

Practice a complete Extract → Clean → Transform → Validate → Load pipeline
using the public [JSONPlaceholder](https://jsonplaceholder.typicode.com/) REST API
as the data source.

## Instructions

1. Open `solution.ipynb` in Jupyter Notebook or Google Colab.
2. Run every cell from top to bottom.
3. Fill in the **TODO** sections with your own transformations.
4. Save the final output CSV in `../../data/output/`.
5. Write your findings in the **Summary & Findings** section.

## Submission Checklist

- [ ] Notebook cells all run without errors
- [ ] Output CSV present in `data/output/`
- [ ] Summary section completed
- [ ] Notebook saved and submitted

## Expected Output Columns

| Column | Description |
|--------|-------------|
| `id` | Post identifier |
| `userid` | Author identifier |
| `title` | Post title (cleaned) |
| `body_length` | Character count of the post body |
