# M1-M5 Demo Recording Steps

## Before Recording

1. Start the combined M1/M2 app at port 8503, API at 8002, Career Guidance app at 8501, and College Admin Dashboard at 8502 using the local instructions in `MILESTONE_3_4.md`.
2. Open `http://localhost:8503`, `http://localhost:8501`, and `http://localhost:8502` in separate browser tabs.
3. Verify the catalog contains JNTU Hyderabad CSE and MGIT Hyderabad CSE, plus the CBIT Hyderabad and OU Hyderabad sample records. Fee and placement figures appear only when present in the admin catalog.
4. Use a fresh demo student account/query when you want to demonstrate a new purchase. Existing purchases are restored from memory and skip the new-purchase path.

## Suggested Recording Sequence

1. Start on the M1 Agent Foundation page at `http://localhost:8503`. Show the four foundational agents and their workflow overview.
2. Open the M2 Tools Hub. Show the nine listed tools and accurately note that the current UI has five active tools and four inactive/planned tools. Demonstrate an available operation such as creating a 5-day Python study plan with Study Planner.
3. Explain that M2 and M3 are separate flows. M3 accepts a career query independently; do not imply an M2 request or authenticated M1 profile is handed into the current M3 workflow.
4. Open Career Guidance v2.0 at `http://localhost:8501` and enter `My name is Alex, I scored 85 percent in Intermediate MPC from Hyderabad. I am interested in CSE. Please generate my personalized career roadmap with best colleges including MGIT Hyderabad, skills to learn, and placement details.`
5. Select **Generate My Career Roadmap**. Show the five-agent flow and Tool Result with CSE college matches, Alex's name, CSE skills, entrance exams, and four-year roadmap. Confirm employee records are absent and that college fee/placement values come from the catalog rather than being invented.
6. Select **My Roadmap** if it is not already open, and show the free preview and payment action.
7. Select **Buy Personalized Roadmap - Rs. 150**. In the demo payment dialog, show the amount, select a payment method, and select **Generate Now - Rs. 150**.
8. Show payment verification success, then select **View My Roadmap** to display the unlocked roadmap.
9. Open the College Admin Dashboard at `http://localhost:8502`. Show analytics, then open **College Catalog** and demonstrate add/edit/delete controls without deleting the seeded demo colleges.
10. Optionally finish with `/docs`, `/health`, and `/monitoring/summary` on port 8002.

## Recording Notes

- The Rs. 150 payment flow is a local academic-project simulation. Do not describe it as a real payment or process real financial details.
- Do not record API keys, environment files, private student records, or personal browser notifications.
- Do not reuse the already-purchased exact MPC query when demonstrating the new-payment branch. Long-term memory intentionally unlocks an existing purchase without charging again.
- M2-to-M3 is intentionally a navigation/demo sequence, not a data handoff: the M3 career query must be typed independently.