## Profiling

Run the server with the following command.

```bash
python ./manage.py runprofileserver --use-cprofile --prof-path=profile-data
```

and proceed with the load testing as usual. Then run the following command from `testsite` to generate the profiling report in `prof_report.txt`.

```bash
python view_profile_stats.py
```

For a summary of total time spent inside each file of `django`, run the following command from `testsite`.

```bash
python django_profile_stats.py
```

This will emit a JSON file `django_prof_report.json`.
