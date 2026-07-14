<?php
/**
 * Seeds a starter adoption curriculum into Tutor LMS.
 *
 * Run automatically by setup.sh, or on demand:
 *     ./setup.sh seed
 *
 * HOW TO CUSTOMIZE:
 *   Edit the $CURRICULUM array below. Each course has topics; each topic has
 *   lessons. Re-running is safe — courses/topics/lessons already present
 *   (matched by title) are skipped, not duplicated.
 *
 * Tutor LMS post types used:
 *   - 'courses'  a course        (top level)
 *   - 'topics'   a topic/section  (child of a course)
 *   - 'lesson'   a lesson         (child of a topic)
 */

if (!post_type_exists('courses')) {
    fwrite(STDERR, "Tutor LMS is not active — cannot seed. Activate it first.\n");
    return;
}

// ---------------------------------------------------------------------------
// EDIT ME: your curriculum. This is a skeleton to replace with real content.
// ---------------------------------------------------------------------------
$CURRICULUM = [
    [
        'title'       => 'Understanding Adoption: An Adoptee-Centered Foundation',
        'description' => 'A foundational course on the lived experience of adoption — for adoptive parents, counselors, and adoptees. Replace this description and the lessons below with your own material.',
        'topics' => [
            [
                'title'   => 'Module 1 — The Adoptee Experience',
                'lessons' => [
                    'What adoption feels like from the inside',
                    'Memory, silence, and the stories we tell ourselves',
                    'The primal wound and early separation',
                ],
            ],
            [
                'title'   => 'Module 2 — Attachment & Identity',
                'lessons' => [
                    'Attachment after disrupted early bonds',
                    'Identity formation across the lifespan',
                    'Search, reunion, and the birth family',
                ],
            ],
            [
                'title'   => 'Module 3 — For Adoptive Parents',
                'lessons' => [
                    'Talking about adoption at every age',
                    'Honoring the child’s history instead of erasing it',
                    'Recognizing and supporting grief',
                ],
            ],
            [
                'title'   => 'Module 4 — Clinical & Support Perspectives',
                'lessons' => [
                    'Adoption-competent counseling basics',
                    'Trauma-informed approaches',
                    'Resources, referrals, and community',
                ],
            ],
        ],
    ],
];
// ---------------------------------------------------------------------------

/** Find an existing post of a type by exact title (optionally under a parent). */
function seed_find_post($title, $post_type, $parent = 0) {
    $q = new WP_Query([
        'post_type'      => $post_type,
        'title'          => $title,
        'post_parent'    => $parent,
        'post_status'    => ['publish', 'draft'],
        'posts_per_page' => 1,
        'no_found_rows'  => true,
    ]);
    return $q->have_posts() ? $q->posts[0]->ID : 0;
}

$created = ['courses' => 0, 'topics' => 0, 'lessons' => 0];

foreach ($CURRICULUM as $course) {
    $course_id = seed_find_post($course['title'], 'courses');
    if (!$course_id) {
        $course_id = wp_insert_post([
            'post_type'    => 'courses',
            'post_status'  => 'publish',
            'post_title'   => $course['title'],
            'post_content' => $course['description'] ?? '',
        ]);
        // Sensible Tutor defaults so the course opens cleanly in the builder.
        update_post_meta($course_id, '_tutor_course_price_type', 'free');
        update_post_meta($course_id, '_tutor_course_level', 'all_levels');
        $created['courses']++;
        echo "Course:  {$course['title']}\n";
    } else {
        echo "Course:  {$course['title']} (exists — skipped)\n";
    }

    $topic_order = 0;
    foreach ($course['topics'] as $topic) {
        $topic_id = seed_find_post($topic['title'], 'topics', $course_id);
        if (!$topic_id) {
            $topic_id = wp_insert_post([
                'post_type'   => 'topics',
                'post_status' => 'publish',
                'post_title'  => $topic['title'],
                'post_parent' => $course_id,
                'menu_order'  => $topic_order,
            ]);
            $created['topics']++;
            echo "  Topic:  {$topic['title']}\n";
        }
        $topic_order++;

        $lesson_order = 0;
        foreach ($topic['lessons'] as $lesson_title) {
            if (!seed_find_post($lesson_title, 'lesson', $topic_id)) {
                wp_insert_post([
                    'post_type'    => 'lesson',
                    'post_status'  => 'publish',
                    'post_title'   => $lesson_title,
                    'post_parent'  => $topic_id,
                    'menu_order'   => $lesson_order,
                    'post_content' => '<p>Lesson content goes here. Edit in Tutor LMS → Courses.</p>',
                ]);
                $created['lessons']++;
                echo "    Lesson: {$lesson_title}\n";
            }
            $lesson_order++;
        }
    }
}

echo "\nDone. Added {$created['courses']} course(s), {$created['topics']} topic(s), {$created['lessons']} lesson(s).\n";
