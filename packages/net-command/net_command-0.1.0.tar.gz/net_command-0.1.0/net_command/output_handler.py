def print_output(results):
    for command, outputs in results.items():
        if isinstance(outputs[0], list):
            print("=" * 10 + f" {command} " + "=" * 10)
            for output_set in outputs:
                for output in output_set:
                    print(output)
                    print("-" * 20)
        else:
            print("=" * 10 + f" {command} " + "=" * 10)
            for output in outputs:
                print(output)
                print("-" * 20)
    print("=" * 20)
