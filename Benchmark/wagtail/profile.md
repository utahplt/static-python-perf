## Profiling

Run the server with the following command:

```bash
python ./manage.py runprofileserver --use-cprofile --prof-path=profile-data
```

and proceed with the load testing as usual. Then run the following command to generate the profiling report in `prof_report.txt`:

```bash
python view_profile_stats.py
```
