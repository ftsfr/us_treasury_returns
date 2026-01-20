"""
Downloads treasury auction data from TreasuryDirect.gov
See here: https://treasurydirect.gov/TA_WS/securities/jqsearch

Key Auction Terminology:
- Tendered: The amount bid or submitted in an auction. This is what bidders want to buy.
- Accepted: The amount actually awarded or allocated to bidders. This is what they actually get.
- The difference occurs because auctions can be oversubscribed (more bids than securities available).

What is SOMA?
SOMA (System Open Market Account) is the Federal Reserve's portfolio of securities used to
implement monetary policy. When the Fed participates in Treasury auctions:
- It typically bids non-competitively (accepts whatever rate/yield is determined)
- Purchases inject money into the banking system (expansionary policy)
- Sales or non-replacement of maturing securities drain money (contractionary policy)
- SOMA data helps researchers track Fed monetary policy implementation and its market impact

Data Dictionary:

Core Identifiers:
- cusip: Unique 9-character identifier for each security (Committee on Uniform Securities Identification Procedures)
- announcedCusip: CUSIP announced at time of auction announcement (may differ from final CUSIP)
- originalCusip: CUSIP from original issue (for reopened securities)
- corpusCusip: CUSIP for the principal portion of a stripped security

Security Information:
- securityType: Type of marketable security (Bill, Note, Bond, TIPS, FRN)
- securityTerm: Term of the security (e.g., "4-Week", "2-Year", "30-Year")
- securityTermDayMonth: Security term expressed in days/months format
- securityTermWeekYear: Security term expressed in weeks/years format
- series: Series designation for notes (letter + year of maturity)
- type: Additional security type classification
- term: Alternative term designation
- originalSecurityTerm: Original term for reopened securities

Key Dates:
- issueDate: Date security is delivered to buyer's account
- maturityDate: Date security stops earning interest and principal is repaid
- announcementDate: Date auction is announced to public
- auctionDate: Date auction is conducted
- auctionDateYear: Year of the auction
- datedDate: Date interest begins accruing (usually same as issue date)
- maturingDate: Date of maturing securities being replaced
- firstInterestPaymentDate: Date of first interest payment (for notes/bonds)
- originalIssueDate: First issue date for reopened securities
- originalDatedDate: Original dated date for reopened securities
- callDate: Date bond can be called (pre-1985 bonds)
- calledDate: Date bond was actually called
- backDatedDate: Date for backdated securities

Interest/Rate Information:
- interestRate: Annual interest rate (percentage) for notes/bonds/TIPS
- refCpiOnIssueDate: Reference CPI on issue date (TIPS only)
- refCpiOnDatedDate: Reference CPI on dated date (TIPS only)
- indexRatioOnIssueDate: Index ratio on issue date (TIPS only)
- interestPaymentFrequency: Frequency of interest payments
- firstInterestPeriod: Length of first interest period
- standardInterestPaymentPer1000: Standard interest payment per $1,000 face value
- spread: Fixed spread over index rate (FRNs only)
- frnIndexDeterminationDate: Date index rate determined (FRNs)
- frnIndexDeterminationRate: Index rate used (FRNs)

Accrued Interest:
- accruedInterestPer1000: Accrued interest per $1,000 (unadjusted)
- accruedInterestPer100: Accrued interest per $100 (unadjusted)
- adjustedAccruedInterestPer1000: Inflation-adjusted accrued interest (TIPS)
- unadjustedAccruedInterestPer1000: Unadjusted accrued interest (TIPS)

Auction Results - Rates/Yields:
- averageMedianDiscountRate: Median discount rate (bills) or average in multiple-price auction
- averageMedianInvestmentRate: Median investment rate (bills)
- averageMedianPrice: Median price accepted
- averageMedianDiscountMargin: Median discount margin (FRNs)
- averageMedianYield: Median yield (notes/bonds/TIPS)
- highDiscountRate: Highest discount rate accepted (bills)
- highInvestmentRate: Highest investment rate accepted (bills)
- highPrice: Highest price accepted
- highDiscountMargin: Highest discount margin accepted (FRNs)
- highYield: Highest yield accepted (notes/bonds/TIPS)
- lowDiscountRate: Lowest discount rate accepted (bills)
- lowInvestmentRate: Lowest investment rate accepted (bills)
- lowPrice: Lowest price accepted
- lowDiscountMargin: Lowest discount margin accepted (FRNs)
- lowYield: Lowest yield accepted (notes/bonds/TIPS)

Pricing:
- adjustedPrice: Inflation-adjusted price (TIPS)
- unadjustedPrice: Price before inflation adjustment (TIPS)
- pricePer100: Price per $100 face value

Auction Statistics:
- totalAccepted: Total dollar amount actually sold in the auction
- totalTendered: Total dollar amount of all bids received (demand)
- bidToCoverRatio: Ratio showing auction demand (totalTendered/totalAccepted)
- allocationPercentage: Percentage allocated at high rate/yield when oversubscribed
- allocationPercentageDecimals: Number of decimal places in allocation percentage

Bidder Categories:
- competitiveAccepted: Dollar amount awarded to competitive bidders (who specify rate/yield)
- competitiveTendered: Dollar amount competitive bidders tried to buy
- competitiveTendersAccepted: Number of competitive bids that were successful
- competitiveBidDecimals: Decimal places allowed in competitive bids
- noncompetitiveAccepted: Dollar amount awarded to noncompetitive bidders (who accept any rate)
- noncompetitiveTendersAccepted: Number of noncompetitive bids that were successful
- primaryDealerAccepted: Amount awarded to primary dealers (large banks/brokers)
- primaryDealerTendered: Amount primary dealers bid for
- directBidderAccepted: Amount awarded to direct bidders (bid directly with Treasury)
- directBidderTendered: Amount direct bidders bid for
- indirectBidderAccepted: Amount awarded to indirect bidders (bid through intermediaries)
- indirectBidderTendered: Amount indirect bidders bid for
- treasuryRetailAccepted: Amount awarded to individual investors via TreasuryDirect
- treasuryRetailTendersAccepted: Number of successful TreasuryDirect bids

Federal Reserve & Foreign:
- somaAccepted: Dollar amount the Fed was awarded in this auction
- somaTendered: Dollar amount the Fed bid for in this auction
- somaIncluded: Boolean indicating if the Fed participated in this auction
- somaHoldings: Fed's current holdings of this specific security
- fimaIncluded: Whether foreign/international accounts included
- fimaNoncompetitiveAccepted: Foreign/international noncompetitive accepted
- fimaNoncompetitiveTendered: Foreign/international noncompetitive tendered

Auction Parameters:
- offeringAmount: Total amount offered in auction
- minimumBidAmount: Minimum bid amount allowed
- maximumCompetitiveAward: Maximum competitive award to single bidder
- maximumNoncompetitiveAward: Maximum noncompetitive award
- maximumSingleBid: Maximum single bid amount
- multiplesToBid: Required bid increment
- multiplesToIssue: Required issue increment
- minimumToIssue: Minimum amount that will be issued
- minimumStripAmount: Minimum amount for stripping
- currentlyOutstanding: Amount currently outstanding
- estimatedAmountOfPubliclyHeldMaturingSecuritiesByType: Estimate of maturing securities

Auction Timing:
- closingTimeCompetitive: Closing time for competitive bids
- closingTimeNoncompetitive: Closing time for noncompetitive bids
- auctionFormat: Format of auction (single-price, multiple-price)

Special Features:
- reopening: Boolean indicating if this is a reopening
- cashManagementBillCMB: Boolean for cash management bills
- floatingRate: Boolean for floating rate notes
- tips: Boolean for Treasury Inflation-Protected Securities
- callable: Boolean if bond is callable
- backDated: Boolean if security is backdated
- strippable: Boolean if security can be stripped

TIPS-Specific:
- cpiBaseReferencePeriod: Base reference period for CPI
- tiinConversionFactorPer1000: TIIN conversion factor per $1,000

Position Reporting:
- nlpExclusionAmount: Net long position exclusion amount
- nlpReportingThreshold: Net long position reporting threshold

Documentation:
- pdfFilenameAnnouncement: PDF file for auction announcement
- pdfFilenameCompetitiveResults: PDF file for competitive results
- pdfFilenameNoncompetitiveResults: PDF file for noncompetitive results
- pdfFilenameSpecialAnnouncement: PDF file for special announcements
- xmlFilenameAnnouncement: XML file for auction announcement
- xmlFilenameCompetitiveResults: XML file for competitive results
- xmlFilenameSpecialAnnouncement: XML file for special announcements

STRIPS Components:
- tintCusip1: CUSIP for first interest component
- tintCusip2: CUSIP for second interest component
- tintCusip1DueDate: Due date for first interest component
- tintCusip2DueDate: Due date for second interest component

Metadata:
- updatedTimestamp: Timestamp of last update
"""

import json
import urllib.request
from pathlib import Path

import pandas as pd

import chartbook

BASE_DIR = chartbook.env.get_project_root()
DATA_DIR = BASE_DIR / "_data"


def pull_treasury_auction_data():
    url = "https://treasurydirect.gov/TA_WS/securities/jqsearch?format=jsonp"

    with urllib.request.urlopen(url) as wpg:
        x = wpg.read()
        data = json.loads(x.replace(b");", b"").replace(b"callback (", b""))

    df = pd.DataFrame(data["securityList"])

    # Date columns
    date_cols = [
        "issueDate",
        "maturityDate",
        "announcementDate",
        "auctionDate",
        "datedDate",
        "backDatedDate",
        "callDate",
        "calledDate",
        "firstInterestPaymentDate",
        "maturingDate",
        "originalDatedDate",
        "originalIssueDate",
        "tintCusip1DueDate",
        "tintCusip2DueDate",
    ]
    df[date_cols] = df[date_cols].apply(pd.to_datetime, errors="coerce")

    # Numeric columns (percentages and amounts)
    numeric_cols = [
        "interestRate",
        "accruedInterestPer1000",
        "accruedInterestPer100",
        "adjustedAccruedInterestPer1000",
        "adjustedPrice",
        "allocationPercentage",
        "averageMedianDiscountRate",
        "averageMedianInvestmentRate",
        "averageMedianPrice",
        "bidToCoverRatio",
        "totalAccepted",
        "totalTendered",
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Boolean columns
    bool_cols = [
        "backDated",
        "callable",
        "cashManagementBillCMB",
        "fimaIncluded",
        "floatingRate",
        "reopening",
        "somaIncluded",
        "strippable",
        "tips",
    ]
    for col in bool_cols:
        df[col] = df[col].map({"true": True, "false": False})

    return df


def load_treasury_auction_data(data_dir: Path = DATA_DIR):
    """
    Load treasury auction data from parquet file.
    """
    df = pd.read_parquet(data_dir / "treasury_auction_stats.parquet")
    return df


def _demo():
    # Set display options to show all columns
    pd.set_option("display.max_columns", None)  # Show all columns
    pd.set_option("display.width", None)  # Don't wrap to multiple lines
    pd.set_option("display.max_rows", None)  # Show all rows

    df = load_treasury_auction_data()
    df.dtypes
    df.info()


if __name__ == "__main__":
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    df = pull_treasury_auction_data()
    df.to_parquet(DATA_DIR / "treasury_auction_stats.parquet", index=False)
