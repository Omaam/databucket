"""Example for DataBucket.
"""
import databucket as db


def main():

    j1820 = db.Bucket(object="MAXI J1820+070")

    # Event
    event = j1820.request_event(obsid="1200120106")
    df = event.to_pandas()
    print(df)

    # Curve
    table = j1820.request_curve(obsid="1200120106", dt=1e3,
                                energy_range_kev=[0.5, 10],
                                save_to="../fits/")
    df = table.to_pandas()
    print(df)


if __name__ == "__main__":
    main()
