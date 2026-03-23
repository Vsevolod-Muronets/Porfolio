def make_report():
    from analytics import analysis 
    from config import num_of_steps, report_template
    
    try:
        Research, file_pth = analysis()
        
        if file_pth == None:
            return

        research = Research(file_pth)
        data = research.file_reader()

        if not data or isinstance(data[0], str):
            print(data[0])
            return

        if not any(row[0] for row in data) and not any(row[1] for row in data):
            print(data[0])
            return

        analytics = research.Analytics(data)
        heads, tails = analytics.counts()
        head_fraction, tail_fraction = analytics.fractions(heads, tails)

        predictions = analytics.predict_random(num_of_steps)
        predicted_heads = sum(row[0] for row in predictions if row[0] == 1)
        predicted_tails = sum(row[1] for row in predictions if row[1] == 1)

        report = report_template.format(
            observations=len(data),
            heads=heads,
            tails=tails,
            heads_percent=head_fraction,
            tails_percent=tail_fraction,
            steps=num_of_steps,
            predicted_heads=predicted_heads,
            predicted_tails=predicted_tails
        )

        analytics.save_file([report], 'report', 'txt')

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    make_report()
