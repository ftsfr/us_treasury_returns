# US Treasury Returns Pipeline

This pipeline downloads and processes US Treasury bond returns from CRSP via WRDS.

## Data Source

- CRSP US Treasury Database (via WRDS)
- Treasury auction data from TreasuryDirect.gov

## Outputs

- `ftsfr_treas_bond_returns.parquet`: Individual Treasury bond monthly returns
- `ftsfr_treas_bond_portfolio_returns.parquet`: Portfolio returns by maturity group
- `treasury_auction_stats.parquet`: Treasury auction statistics
- `treasuries_with_run_status.parquet`: On-the-run/off-the-run status

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your WRDS username
   ```

3. Run the pipeline:
   ```bash
   doit
   ```

4. View the generated documentation in `docs/index.html`

## Data Coverage

- Time period: 1970 - present
- Frequency: Daily (aggregated to monthly)
- Granularity: Individual Treasury notes and bonds

## Portfolio Groupings

Bonds are grouped into 10 maturity buckets (6-month intervals from 0-5 years):
- Group 1: 0 to 6 months
- Group 2: 6 months to 1 year
- ...
- Group 10: 4.5 to 5 years
