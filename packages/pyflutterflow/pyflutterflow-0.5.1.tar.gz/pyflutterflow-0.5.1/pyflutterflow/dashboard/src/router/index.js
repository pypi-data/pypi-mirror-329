import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store';
import HomeView from '@/views/HomeView.vue';
import DatabaseEntityIndex from '@/views/DatabaseEntityIndex.vue';
import DatabaseEntityDetail from '@/views/DatabaseEntityDetail.vue';
import UserIndex from '@/views/UserIndex.vue';
import UserDetail from '@/views/UserDetail.vue';
import LoginView from '@/views/AuthViews/LoginView.vue';
import ProfileView from '@/views/AuthViews/ProfileView.vue';
import TermsAndConds from '@/views/TermsAndConds.vue';
import PrivacyPolicy from '@/views/PrivacyPolicy.vue';
import SendNotification from '@/views/SendNotification.vue';
import NotFound404 from '@/views/NotFound404.vue';

const router = createRouter({
  history: createWebHistory('/dashboard'),
  routes: [
    {
      path: '/',
      name: 'HomeView',
      component: HomeView,
      meta: { requiresAuth: true, requiresVerifiedEmail: true},
    },
    {
      path: '/send-notification',
      name: 'SendNotification',
      component: SendNotification,
      meta: { requiresAuth: true, requiresVerifiedEmail: true},
    },
    {
      path: '/app-compliance/terms-and-conditions',
      name: 'TermsAndConds',
      component: TermsAndConds,
      meta: { requiresAuth: true, requiresVerifiedEmail: true},
    },
    {
      path: '/app-compliance/privacy-policy',
      name: 'PrivacyPolicy',
      component: PrivacyPolicy,
      meta: { requiresAuth: true, requiresVerifiedEmail: true},
    },
    {
      path: '/firebase-users',
      name: 'UserIndex',
      component: UserIndex,
      meta: { requiresAuth: true },
    },
    {
      path: '/firebase-users/:uid',
      name: 'UserDetail',
      component: UserDetail,
      meta: { requiresAuth: true },
    },
    {
      path: '/:entity',
      name: 'DatabaseEntityIndex',
      component: DatabaseEntityIndex,
      meta: { requiresAuth: true },
    },
    {
      path: '/:entity/:id',
      name: 'DatabaseEntityDetail',
      component: DatabaseEntityDetail,
      meta: { requiresAuth: true },
    },
    {
      path: '/auth',
      name: 'AuthLayout',
      children: [
        {
          path: 'login',
          name: 'LoginView',
          component: LoginView
        },
        {
          path: 'profile',
          name: 'ProfileView',
          component: ProfileView
        },
      ]
    },
    {
      path: '/:catchAll(.*)*', // This will match everything and act as a catch-all route
      name: 'NotFound404',
      component: NotFound404,
      meta: { requiresAuth: true },
    }
  ]
})


router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore();

  if (!authStore.user)
    await authStore.checkForAuthenticatedUser();

  const requiresEmailVerification = to.matched.some(record => record.meta.requiresVerifiedEmail);

  if (requiresEmailVerification && authStore.user && !authStore.user.emailVerified) {
    authStore.setEmailVerificationModal(true);
    next(false);
    return;
  }
  authStore.setEmailVerificationModal(false);

  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  if (requiresAuth && !authStore.user) {
    next({ name: 'LoginView', query: { redirect: to.fullPath } });
    return;
  }


  next();
});

export default router
