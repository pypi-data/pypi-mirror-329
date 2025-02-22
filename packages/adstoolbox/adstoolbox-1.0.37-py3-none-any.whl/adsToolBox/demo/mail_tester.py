import requests
import imaplib

TENANT_ID = "7638e353-5319-43ae-b3d3-2ac7fd0ac61f"
CLIENT_ID = "d01021f8-4d0d-4371-a2a8-df64a370f432"
CLIENT_SECRET = "9o98Q~767iNq9_SCntzLEEjnfziMSBDOWf3FlaD5"

TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"

payload = {
    'grant_type': 'client_credentials',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'scope': 'https://outlook.office365.com/.default'
}

response = requests.post(TOKEN_URL, data=payload)
token_data = response.json()

if "access_token" in token_data:
    ACCESS_TOKEN = token_data["access_token"]
    print("Token obtenu avec succès !")
else:
    print("Erreur :", token_data)
    ACCESS_TOKEN = None

if ACCESS_TOKEN:
    IMAP_SERVER = "outlook.office365.com"
    EMAIL = "echange@terralacta.com"

    try:
        imap_conn = imaplib.IMAP4_SSL(IMAP_SERVER)
        auth_string = f"user={EMAIL}\1auth=Bearer {ACCESS_TOKEN}\1\1"
        imap_conn.authenticate("XOAUTH2", lambda x: auth_string.encode("utf-8"))

        imap_conn.select(readonly=True)  # True implique qu'un mail lu restera en UnSeen
        imap_conn.select("INBOX")

        status, email_ids = imap_conn.search(None, "UnSeen")
        print("Emails non lus :", email_ids)

        """
        to_restore = "2584 2585 2586 2587 2588 2589 2590 2591 2592 2593 2594 2595 2596 2597 2598 2599 2600 2601 2602 2603 2604 2605 2606 2607 2608 2609 2610 2611 2612 2613 2614 2615 2616 2617 2618 2619 2620 2621 2622 2623 2624 2625 2626 2627 2628 2629 2630 2631 2632 2633 2634 2635 2636 2637 2638 2639 2640 2641 2642 2643 2644 2645 2646 2647 2648 2649 2650 2651 2652 2653 2654 2655 2656 2657 2658 2659 2660 2661 2662 2663 2664 2665 2666 2667 2668 2669 2670 2671 2672 2673 2674 2675 2676 2677 2678 2679 2680 2681 2682 2683 2684 2685 2686 2687 2688 2689 2690 2691 2692 2693 2694 2695 2696 2697 2698 2699 2700 2701 2702 2703 2704 2705 2706 2707 2708 2709 2710 2711 2712 2713 2714 2715 2716 2717 2718 2719 2720 2721 2722 2723 2724 2725 2726 2727 2728 2729 2730 2731 2732 2736 2737 2738 2739 2740 2741 2742 2743 2744 2745 2746 2747 2748 2749 2750 2751 2752 2753 2754 2755 2756 2757 2758 2759 2760 2761 2763 2764 2765 2766 2767 2768 2769 2770 2771 2772 2773 2774 2775 2776 2777 2778 2779 2780 2781 2782 2783 2784 2785 2786 2787 2788 2789 2790 2791 2792 2793 2794 2795 2796 2797 2798 2799 2800 2801 2802 2803 2804 2805 2806 2807 2808 2809 2810 2811 2812 2813 2814 2815 2816 2817 2818 2819 2820 2821 2822 2823 2824 2825 2826 2827 2828 2829 2830 2831 2832 2833 2834 2835 2836 2837 2838 2839 2840 2841 2842 2843 2844 2845 2846 2847 2848 2852 2853 2854 2855 2856"
        to_restore = "2852 2853 2854 2855 2856"
        to_restore = to_restore.split(' ')
        for email in to_restore:
            imap_conn.store(email, '-FLAGS', '\\Seen')
        """
        # Déconnexion
        imap_conn.logout()
    except Exception as e:
        print("Erreur de connexion IMAP :", str(e))
else:
    print("Impossible de se connecter : Token OAuth2 manquant.")