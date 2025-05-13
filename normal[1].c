int score = 72;
int attendance = 85;
printf("%d\n", score);
printf("%d\n", attendance);
printf("Checking student eligibility...\n");

void evaluate(int score, int attendance) {
    if (score >= 50) {
        printf("Score meets the requirement\n");

        if (attendance >= 75) {
            printf("Attendance is sufficient\n");
            printf("Student is eligible for exam\n");
        } else {
            printf("Attendance is too low\n");
            printf("Student is not eligible despite good score\n");
        }

    } else {
        printf("Score is too low\n");
        printf("Student is not eligible for exam\n");
    }
}
