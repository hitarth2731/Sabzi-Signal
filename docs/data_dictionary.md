# Data Dictionary: Mandi Prices (data.gov.in / Agmarknet)

**Source:** data.gov.in API, resource "Current Daily Price of Various Commodities from Various Markets (Mandi)"
**Grain:** One row = one commodity, of one variety and grade, sold at one market on one arrival date, with that day's min, max and modal price.

| Field        | Type (raw) | Example            | Meaning                   | Notes / cleaning needed                                             |
| ------------ | ---------- | ------------------ | ------------------------- | ------------------------------------------------------------------- |
| state        | text       | Keralam            | State of the market       | Spelling may differ across sources (Kerala/Keralam), so standardize |
| district     | text       | Kozhikode(Calicut) | District of the market    | Contains alternate names in brackets                                |
| market       | text       | Mukkom Market      | Mandi (APMC market) name  |                                                                     |
| commodity    | text       | Ginger(Green)      | Product traded            | Filter for Tomato, Onion                                            |
| variety      | text       | Green Ginger       | Variety of the commodity  |                                                                     |
| grade        | text       | FAQ                | Quality grade             | FAQ = Fair Average Quality                                          |
| arrival_date | text       | 24/11/2026         | Date of the prices        | DD/MM/YYYY stored as text, so convert with an explicit format       |
| min_price    | number     | 12000              | Lowest price that day     | ₹ per quintal (100 kg)                                              |
| max_price    | number     | 13000              | Highest price that day    | ₹ per quintal                                                       |
| modal_price  | number     | 12500              | Most common trading price | ₹ per quintal; **main metric**; ₹/kg = modal_price / 100            |

## Validity rules to check later

- min_price ≤ modal_price ≤ max_price
- Prices > 0
- arrival_date is a valid date and not in the future
