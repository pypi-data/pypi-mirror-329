Consider:

import duckdb

sql = """
select
id,
address_concat,
regexp_split_to_array(upper(trim(address_concat)), '\\s+') as address_tokens,
postcode,

from df

"""
duckdb.sql(sql).show(max_width=100000)

┌───────┬─────────────────────────────────────────────┬─────────────────────────────────────────────────────┬──────────┐
│  id   │               address_concat                │                   address_tokens                    │ postcode │
│ int64 │                   varchar                   │                      varchar[]                      │ varchar  │
├───────┼─────────────────────────────────────────────┼─────────────────────────────────────────────────────┼──────────┤
│     1 │ 57 GUNTERSTONE ROAD LONDON                  │ [57, GUNTERSTONE, ROAD, LONDON]                     │ W14 9BS  │
│     2 │ 41 GUNTERSTONE ROAD LONDON                  │ [41, GUNTERSTONE, ROAD, LONDON]                     │ W14 9BS  │
│     3 │ 71 GUNTERSTONE ROAD LONDON                  │ [71, GUNTERSTONE, ROAD, LONDON]                     │ W14 9BS  │
│     4 │ FLAT BASEMENT 39 BLUNDERTON ROAD LONDON     │ [FLAT, BASEMENT, 39, BLUNDERTON, ROAD, LONDON]      │ W14 9XY  │
│     5 │ FLAT GROUND FLOOR 39 BLUNDERTON ROAD LONDON │ [FLAT, GROUND, FLOOR, 39, BLUNDERTON, ROAD, LONDON] │ W14 9XY  │
│     6 │ FLAT THIRD FLOOR 39 BLUNDERTON ROAD LONDON  │ [FLAT, THIRD, FLOOR, 39, BLUNDERTON, ROAD, LONDON]  │ W14 9XY  │
│     7 │ FLAT 4 39 BLUNDERTON ROAD LONDON            │ [FLAT, 4, 39, BLUNDERTON, ROAD, LONDON]             │ W14 9XY  │
│     8 │ 5 LOVE LANE KINGS LANGLEY                   │ [5, LOVE, LANE, KINGS, LANGLEY]                     │ WD4 9HW  │
│     9 │ 7 LOVE LANE KINGS LANGLEY                   │ [7, LOVE, LANE, KINGS, LANGLEY]                     │ WD4 9HW  │
│    10 │ 9 LOVE LANE KINGS LANGLEY                   │ [9, LOVE, LANE, KINGS, LANGLEY]                     │ WD4 9HW  │
│    11 │ MILLSTONE LOVE LANE KINGS LANGLEY           │ [MILLSTONE, LOVE, LANE, KINGS, LANGLEY]             │ WD4 9HW  │
│    12 │ MAYTREES LOVE LANE KINGS LANGLEY            │ [MAYTREES, LOVE, LANE, KINGS, LANGLEY]              │ WD4 9HW  │
│    13 │ FLAT 1 OPENFIELDS LOVE LANE KINGS LANGLEY   │ [FLAT, 1, OPENFIELDS, LOVE, LANE, KINGS, LANGLEY]   │ WD4 9HW  │
│    14 │ FLAT 2 OPENFIELDS LOVE LANE KINGS LANGLEY   │ [FLAT, 2, OPENFIELDS, LOVE, LANE, KINGS, LANGLEY]   │ WD4 9    │
├───────┴─────────────────────────────────────────────┴─────────────────────────────────────────────────────┴──────────┤
│ 14 rows                                                                                                    4 columns │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

I want to do some address matching of this data to a canonical list of addresses.

One of the major challenges is pulling out the tokens that uniquely identify the address from similar addresses.

By 'similar addresses' I mean those in a group.  This group may be a list of all addresses in a postcode, but doesn't have to be.  It could be, for instance, a list of all addresses within a tiny geographical area, or all addresses that match a very specific search term.

For instnce, if the following addresess are the only ones in a postcode:

57, GUNTERSTONE ROAD, LONDON  W14 9BS  -> '57' uniquely identifies within this group
41, GUNTERSTONE ROAD, LONDON  W14 9BS  -> '41' uniquely identifies within this group
71, GUNTERSTONE ROAD, LONDON  W14 9BS -> '71' unique indentifies within this group


But it's more complex than that because in some cases we may have

FLAT BASEMENT, 39, GUNTERSTONE ROAD, LONDON    ->  'BASEMENT, 39' (or arguably FLAT BASEMENT, 39)
FLAT GROUND FLOOR, 39, GUNTERSTONE ROAD, LONDON -> 'GROUND 39,'  (or arguably FLAT GROUND FLOOR, 39,)
FLAT THIRD FLOOR, 39, GUNTERSTONE ROAD, LONDON  -> 'THIRD 39' (or arguably FLAT THIRD FLOOR, 39)
FLAT 4, 39, GUNTERSTONE ROAD, LONDON -> 'FLAT 4, 39,'

As you can see, this is kind of similar to getting somthing a bit like the 'house number' but more complex

For example, sometimes there is no number:

5, LOVE LANE, KINGS LANGLEY -> '5'
7, LOVE LANE, KINGS LANGLEY -> '7'
9, LOVE LANE, KINGS LANGLEY -> '9'
MILLSTONE, LOVE LANE, KINGS LANGLEY -> 'MILLSTONE'
MAYTREES, LOVE LANE, KINGS LANGLEY -> 'MAYTREES'
FLAT 1 OPENFIELDS, LOVE LANE, KINGS LANGLEY -> '1 OPENFIELDS'
FLAT 2 OPENFIELDS, LOVE LANE, KINGS LANGLEY -> '2 OPENFIELDS'

So, consider this data:

address_concat, postcode, group
57 GUNTERSTONE ROAD LONDON,W14 9BS,1
41 GUNTERSTONE ROAD LONDON,W14 9BS,1
71 GUNTERSTONE ROAD LONDON,W14 9BS,1
FLAT BASEMENT 39 BLUNDERTON ROAD LONDON,W14 9XY,2
FLAT GROUND FLOOR 39 BLUNDERTON ROAD LONDON,W14 9XY,2
FLAT THIRD FLOOR 39 BLUNDERTON ROAD LONDON,W14 9XY,2
FLAT 4 39 BLUNDERTON ROAD LONDON,W14 9XY,2
5 LOVE LANE KINGS LANGLEY, WD4 9HW,3
7 LOVE LANE KINGS LANGLEY, WD4 9HW,3
9 LOVE LANE KINGS LANGLEY, WD4 9HW,3
MILLSTONE LOVE LANE KINGS LANGLEY, WD4 9HW,3
MAYTREES LOVE LANE KINGS LANGLEY, WD4 9HW,3
FLAT 1 OPENFIELDS LOVE LANE KINGS LANGLEY, WD4 9HW,3
FLAT 2 OPENFIELDS LOVE LANE KINGS LANGLEY, WD4 9,3


I think we can approach this problem by somehow looking at the counts of tokens within each group.

Specifically, the 'distinguishing' tokens are those that have a count of 1 within their group.

Here's a first stab at this:

import duckdb

import pandas as pd

# fmt: off
data = [
    {"id": 1, "address_concat": "57 GUNTERSTONE ROAD LONDON", "postcode": "W14 9BS", "grouping": 1},
    {"id": 2, "address_concat": "41 GUNTERSTONE ROAD LONDON", "postcode": "W14 9BS", "grouping": 1},
    {"id": 3, "address_concat": "71 GUNTERSTONE ROAD LONDON", "postcode": "W14 9BS", "grouping": 1},
    {"id": 4, "address_concat": "FLAT BASEMENT 39 BLUNDERTON ROAD LONDON", "postcode": "W14 9XY", "grouping": 2},
    {"id": 5, "address_concat": "FLAT GROUND FLOOR 39 BLUNDERTON ROAD LONDON", "postcode": "W14 9XY", "grouping": 2},
    {"id": 6, "address_concat": "FLAT THIRD TOP FLOOR 39 BLUNDERTON ROAD LONDON", "postcode": "W14 9XY", "grouping": 2},
    {"id": 7, "address_concat": "FLAT 4 39 BLUNDERTON ROAD LONDON", "postcode": "W14 9XY", "grouping": 2},
    {"id": 8, "address_concat": "5 LOVE LANE KINGS LANGLEY", "postcode": "WD4 9HW", "grouping": 3},
    {"id": 9, "address_concat": "7 LOVE LANE KINGS LANGLEY", "postcode": "WD4 9HW", "grouping": 3},
    {"id": 10, "address_concat": "9 LOVE LANE KINGS LANGLEY", "postcode": "WD4 9HW", "grouping": 3},
    {"id": 11, "address_concat": "MILLSTONE LOVE LANE KINGS LANGLEY", "postcode": "WD4 9HW", "grouping": 3},
    {"id": 12, "address_concat": "MAYTREES LOVE LANE KINGS LANGLEY", "postcode": "WD4 9HW", "grouping": 3},
    {"id": 13, "address_concat": "FLAT 1 OPENFIELDS LOVE LANE KINGS LANGLEY", "postcode": "WD4 9HW", "grouping": 3},
    {"id": 14, "address_concat": "FLAT 2 OPENFIELDS LOVE LANE KINGS LANGLEY", "postcode": "WD4 9HW", "grouping": 3},
    {"id": 15, "address_concat": "FLAT 57 57 ANOTHER ROAD LONDON", "postcode": "W14 9BS", "grouping": 4},
    {"id": 16, "address_concat": "41 ANOTHER ROAD LONDON", "postcode": "W14 9BS", "grouping": 4},
    {"id": 17, "address_concat": "71 ANOTHER ROAD LONDON", "postcode": "W14 9BS", "grouping": 4},
]
# fmt: on

df = pd.DataFrame(data)


sql = """
select
id,
address_concat,
regexp_split_to_array(upper(trim(address_concat)), '\\s+') as address_tokens,
postcode,
grouping
from df

"""
df_with_tokens = duckdb.sql(sql)
df_with_tokens.show(max_width=100000)




sql = """
WITH exploded AS (
    SELECT
        id,
        grouping,
        UNNEST(address_tokens) AS token
    FROM df_with_tokens
),
unique_tokens AS (
    SELECT
        grouping,
        ARRAY_AGG(token) AS unique_token_list
    FROM (
        SELECT
            grouping,
            token
        FROM exploded
        GROUP BY grouping, token
        HAVING COUNT(DISTINCT id) = 1
    ) sub
    GROUP BY grouping
)

SELECT
    df_with_tokens.id,
    df_with_tokens.address_concat,
    df_with_tokens.address_tokens,
    df_with_tokens.grouping,
    LIST_INTERSECT(df_with_tokens.address_tokens, ut.unique_token_list) AS distinguishing_tokens
FROM df_with_tokens
LEFT JOIN unique_tokens ut ON df_with_tokens.grouping = ut.grouping;
"""

duckdb.sql(sql).show(max_width=100000)

This results in:

┌───────┬────────────────────────────────────────────────┬─────────────────────────────────────────────────────────┬──────────┬───────────────────────┐
│  id   │                 address_concat                 │                     address_tokens                      │ grouping │ distinguishing_tokens │
│ int64 │                    varchar                     │                        varchar[]                        │  int64   │       varchar[]       │
├───────┼────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┼──────────┼───────────────────────┤
│     1 │ 57 GUNTERSTONE ROAD LONDON                     │ [57, GUNTERSTONE, ROAD, LONDON]                         │        1 │ [57]                  │
│     2 │ 41 GUNTERSTONE ROAD LONDON                     │ [41, GUNTERSTONE, ROAD, LONDON]                         │        1 │ [41]                  │
│     3 │ 71 GUNTERSTONE ROAD LONDON                     │ [71, GUNTERSTONE, ROAD, LONDON]                         │        1 │ [71]                  │
│     4 │ FLAT BASEMENT 39 BLUNDERTON ROAD LONDON        │ [FLAT, BASEMENT, 39, BLUNDERTON, ROAD, LONDON]          │        2 │ [BASEMENT]            │
│     5 │ FLAT GROUND FLOOR 39 BLUNDERTON ROAD LONDON    │ [FLAT, GROUND, FLOOR, 39, BLUNDERTON, ROAD, LONDON]     │        2 │ [GROUND]              │
│     6 │ FLAT THIRD TOP FLOOR 39 BLUNDERTON ROAD LONDON │ [FLAT, THIRD, TOP, FLOOR, 39, BLUNDERTON, ROAD, LONDON] │        2 │ [TOP, THIRD]          │
│     7 │ FLAT 4 39 BLUNDERTON ROAD LONDON               │ [FLAT, 4, 39, BLUNDERTON, ROAD, LONDON]                 │        2 │ [4]                   │
│     8 │ 5 LOVE LANE KINGS LANGLEY                      │ [5, LOVE, LANE, KINGS, LANGLEY]                         │        3 │ [5]                   │
│     9 │ 7 LOVE LANE KINGS LANGLEY                      │ [7, LOVE, LANE, KINGS, LANGLEY]                         │        3 │ [7]                   │
│    10 │ 9 LOVE LANE KINGS LANGLEY                      │ [9, LOVE, LANE, KINGS, LANGLEY]                         │        3 │ [9]                   │
│    11 │ MILLSTONE LOVE LANE KINGS LANGLEY              │ [MILLSTONE, LOVE, LANE, KINGS, LANGLEY]                 │        3 │ [MILLSTONE]           │
│    12 │ MAYTREES LOVE LANE KINGS LANGLEY               │ [MAYTREES, LOVE, LANE, KINGS, LANGLEY]                  │        3 │ [MAYTREES]            │
│    13 │ FLAT 1 OPENFIELDS LOVE LANE KINGS LANGLEY      │ [FLAT, 1, OPENFIELDS, LOVE, LANE, KINGS, LANGLEY]       │        3 │ [1]                   │
│    14 │ FLAT 2 OPENFIELDS LOVE LANE KINGS LANGLEY      │ [FLAT, 2, OPENFIELDS, LOVE, LANE, KINGS, LANGLEY]       │        3 │ [2]                   │
│    15 │ FLAT 57 57 ANOTHER ROAD LONDON                 │ [FLAT, 57, 57, ANOTHER, ROAD, LONDON]                   │        4 │ [57, FLAT]            │
│    16 │ 41 ANOTHER ROAD LONDON                         │ [41, ANOTHER, ROAD, LONDON]                             │        4 │ [41]                  │
│    17 │ 71 ANOTHER ROAD LONDON                         │ [71, ANOTHER, ROAD, LONDON]                             │        4 │ [71]                  │
├───────┴────────────────────────────────────────────────┴─────────────────────────────────────────────────────────┴──────────┴───────────────────────┤
│ 17 rows                                                                                                                                   5 columns │
└─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘



BUT I'VE JUSTED REALISED AND IMPORTANT MODIFICATION THAT NEED MAKING AS FOLLOWs:

This is very easy to compute within a canonical list, particularly if you have postcode.

The question is how to define the 'group' - this could be:

everything in postcode
sort by on reverse string (address_concat[::-1]) and take the 2 preceeding and 2 following
perform blockign to find similar addresses
The group is harder to define if you have a list of messy addreses, particularly if it contains dupes

For instance,
Messy: 9 love lane kings langley hertfordshire wd49hw
Canonical: 9 love lane kings langley wd49hw

'hertfordshire' comes out as a 'unique' token

SOLUTION TO THIS PROBLEM: The unique tokens of interest are ONLY ones that appear in the canonical list, so in the 'hertfordshire ' we can just drop the token i.e. drop tokens from messy address that do not appear in any canonical records in the group

Possibly solutions:

Allow a unique token to be only one in the first n, say for three tokens in an adress
If we can assume the messy addresses do not contain duplicates, and is a long list i.e., we could use reverse string 2 preceeding and 2 following
look (block) for messy within canonical only, and use that as the group.
this almost works, except for the 'hertfordshire' - although maybe we capture that as a 'common end token' anyway
if messy dataset does not contain duplicaetes, look (block) for messy in BOTH messy and canonical. This forms the group, and a unque token is one that appears at most TWICE in the group (because we should have the messy AND its canonical counterpart)
this does not necessrily solve the hertfordshire case, could combine with 'only first three tokens in address'
3 seems most promising but quite computationally intensive. However, we are blocking already so we can use that.

Another potentially promising option is take first (say) 4 tokens of the address, mix messy with canonical, sort by reverse string address, take 2 preceeding and 2 following, and unique tokens can appear at most TWICE in the group

So I think that leaves two viable/promising options:

We apply this algorithm following probabilistic linkage on the blocked groups. Within the blocks, we pick out unique tokens. Where that's a match on unique within group, considerably up the match score. Where non-unqiue, reduce match score.
Assuming no dupes in messy data, we concat messy data with canonical at first step, and reverse sort on address. Unique tokes are ones which appear at most twice . This is computationally cheap and can be done pre-matching (i.e. doesn't require blocking) so worth pursuing. Note, even if there are dupes in messy data but they're rare, this will still mostly work (we'll just miss unique tokens in the case there are dupes in messy data)
In both cases restrict unique tokens which are found to only those within canonical list. A token that only exists in the messy data is useless

Probably next step is to implement both (1) and (2) and see how they work out.
